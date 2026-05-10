import numpy as np
import torch

from helpers import vsumm_helper
from helpers.eval_protocol_helper import (
    compute_rank_metrics_from_gtscore,
    infer_f1_metric_from_key,
    safe_nanmean,
)


def evaluate_mil_cond(model,
                      val_loader,
                      device: str,
                      selection_score_source: str = 'frame',
                      shot_eval_head: str = 'selection'):
    if selection_score_source not in ('frame', 'shot_head'):
        raise ValueError(
            f'Invalid selection_score_source={selection_score_source}; expected frame or shot_head.'
        )
    if shot_eval_head not in ('selection', 'rank'):
        raise ValueError(f'Invalid shot_eval_head={shot_eval_head}; expected selection or rank.')
    model.eval()

    fscore_list = []
    kendall_list = []
    spearman_list = []
    caption_coverage_list = []

    with torch.no_grad():
        for (
            key,
            seq,
            soft_label,
            text_cond,
            text_target,
            all_text_features,
            caption_spans_idx,
            caption_valid_mask,
            gtscore,
            user_summary,
            cps,
            n_frames,
            nfps,
            picks,
            text_cond_mask,
            caption_coverage_ratio,
        ) in val_loader:
            seq_tensor = torch.tensor(seq, dtype=torch.float32).unsqueeze(0).to(device)
            text_cond_tensor = torch.tensor(text_cond, dtype=torch.float32).to(device)
            text_cond_mask_tensor = torch.tensor(
                text_cond_mask,
                dtype=torch.float32,
                device=device,
            )
            caption_coverage_list.append(float(np.asarray(caption_coverage_ratio).item()))

            if selection_score_source == 'shot_head':
                (
                    _instance_logits,
                    _pool_logits,
                    _frame_summary_scores,
                    _bag_logits,
                    _summary_feat,
                    frame_repr,
                ) = model(
                    seq_tensor,
                    text_cond_tensor,
                    text_cond_mask_tensor,
                )
                overlaps, shot_lengths = build_sampled_to_shot_overlap_eval(
                    picks=torch.tensor(picks, dtype=torch.long, device=device),
                    cps=torch.tensor(cps, dtype=torch.long, device=device),
                    n_frames=int(np.asarray(n_frames).item()),
                )
                shot_scores = model.predict_shot_scores(
                    frame_repr=frame_repr,
                    overlaps=overlaps,
                    shot_lengths=shot_lengths,
                    head=shot_eval_head,
                )
                summary_scores = project_shot_scores_to_sampled_scores(
                    shot_scores=shot_scores,
                    overlaps=overlaps,
                ).detach().cpu().numpy().astype(np.float32)
            else:
                summary_scores = model.predict_summary_scores(
                    seq_tensor,
                    text_cond_tensor,
                    text_cond_mask_tensor,
                ).detach().cpu().numpy().astype(np.float32)

            if not np.isfinite(summary_scores).all():
                num_nan = int(np.isnan(summary_scores).sum())
                num_inf = int(np.isinf(summary_scores).sum())
                raise ValueError(
                    f'Non-finite summary_scores for sample {key}: '
                    f'nan={num_nan}, inf={num_inf}, '
                    f'seq_shape={seq.shape}, text_cond_shape={text_cond.shape}'
                )

            picks_np = np.asarray(picks, dtype=np.int32)
            if summary_scores.shape[0] != picks_np.shape[0]:
                raise ValueError(
                    f'Summary score length mismatch for sample {key}: '
                    f'scores={summary_scores.shape[0]} vs picks={picks_np.shape[0]}'
                )

            pred_summ = vsumm_helper.get_keyshot_summ(
                summary_scores,
                cps,
                int(np.asarray(n_frames).item()),
                nfps,
                picks_np,
            )

            if user_summary is None:
                raise ValueError(f'Missing user_summary for evaluation sample: {key}')

            eval_metric = infer_f1_metric_from_key(key)
            fscore = vsumm_helper.get_summ_f1score(
                pred_summ=pred_summ,
                test_summ=user_summary,
                eval_metric=eval_metric,
            )
            fscore_list.append(float(fscore))

            if gtscore is None:
                raise ValueError(f'Missing gtscore for rank evaluation sample: {key}')

            rank_metrics = compute_rank_metrics_from_gtscore(
                pred_scores=summary_scores,
                gtscore=np.asarray(gtscore, dtype=np.float32),
                key=str(key),
            )
            kendall_list.append(rank_metrics['kendall'])
            spearman_list.append(rank_metrics['spearman'])

    return {
        'fscore': float(np.mean(fscore_list)) if fscore_list else 0.0,
        'kendall': safe_nanmean(kendall_list),
        'spearman': safe_nanmean(spearman_list),
        'num_videos': int(len(fscore_list)),
        'num_rank_videos': int(sum(np.isfinite(v) for v in kendall_list)),
        'caption_coverage': float(np.mean(caption_coverage_list)) if caption_coverage_list else 0.0,
    }


def build_sampled_to_shot_overlap_eval(picks: torch.Tensor,
                                       cps: torch.Tensor,
                                       n_frames: int):
    if picks.ndim != 1:
        raise ValueError(f'Expected picks shape [T], got {tuple(picks.shape)}')
    if cps.ndim != 2 or cps.shape[1] != 2:
        raise ValueError(f'Expected cps shape [S, 2], got {tuple(cps.shape)}')
    if int(n_frames) <= 0:
        raise ValueError(f'Invalid n_frames={n_frames}')

    picks = picks.to(torch.long)
    cps = cps.to(torch.long)
    lo = picks
    hi = torch.empty_like(lo)
    hi[:-1] = picks[1:]
    hi[-1] = int(n_frames)

    overlaps = []
    for shot_idx in range(cps.shape[0]):
        first = int(cps[shot_idx, 0].item())
        last_exclusive = int(cps[shot_idx, 1].item()) + 1
        inter = torch.minimum(hi, lo.new_tensor(last_exclusive)) - torch.maximum(
            lo, lo.new_tensor(first)
        )
        overlaps.append(torch.clamp(inter, min=0).to(torch.float32))
    overlaps = torch.stack(overlaps, dim=0)
    shot_lengths = overlaps.sum(dim=1)
    if not torch.all(shot_lengths > 0):
        raise ValueError('Detected non-positive shot length in evaluation overlap.')
    return overlaps, shot_lengths


def project_shot_scores_to_sampled_scores(shot_scores: torch.Tensor,
                                          overlaps: torch.Tensor) -> torch.Tensor:
    if shot_scores.ndim != 1:
        raise ValueError(f'Expected shot_scores shape [S], got {tuple(shot_scores.shape)}')
    if overlaps.ndim != 2:
        raise ValueError(f'Expected overlaps shape [S, T], got {tuple(overlaps.shape)}')
    if overlaps.shape[0] != shot_scores.shape[0]:
        raise ValueError('Shot count mismatch in project_shot_scores_to_sampled_scores.')
    sample_lengths = overlaps.sum(dim=0).clamp_min(1.0)
    return torch.matmul(overlaps.transpose(0, 1), shot_scores) / sample_lengths
