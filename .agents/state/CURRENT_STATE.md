# MMIL_D Current State

Last updated: 2026-05-10
Owner note: Update this file after every code change, experiment, or corrected understanding.

## Current scientific claim boundary

- Claim type: shot-aware weakly supervised video summarization with sampled-frame scoring and budget-constrained keyshot selection.
- Input/scoring granularity: sampled frames aligned to HDF5 `picks`; model scores have length `T == len(picks)`.
- Weak semantic label granularity: video-level / bag-level soft semantic labels, not human frame-level importance labels.
- Selection granularity: shot/keyshot-level pseudo utility and budgeted pseudo-summary supervision.
- Output granularity: dynamic/keyshot summary generated under the summary budget.
- Allowed training supervision: video-level / bag-level soft semantic labels, dense caption text features, OpenCLIP/VLM-derived pseudo evidence, shot utility that is not constructed from `gtscore` or `user_summary`.
- Disallowed training supervision: `gtscore`, `user_summary`, human frame-level importance score, human summary-derived pseudo labels, human-derived keyshot targets.
- Allowed evaluation/reporting: F1 against `user_summary`, Kendall/Spearman against `gtscore`, provided they are declared as benchmark evaluation or validation model selection.

## Current mainline

Training scripts:

- `scripts/train_mil_cond_summe_tagr.sh`
- `scripts/train_mil_cond_tvsum_tagr.sh`

Paper-facing protocol alignment rule:

- SumMe and TVSum may keep separate dataset launcher scripts, dataset paths, split files, log directories, and benchmark aggregation adapters.
- Paper-facing method claims require the same backbone/training entry, same main training logic, same input feature type and H5 schema, same split policy, same 15 percent summary budget, same keyshot summary-generation flow, and the same main loss/data-flow definition.
- Dataset-specific defaults such as `UTILITY_FORMULA`, seed, and loss weights are allowed only when reported as benchmark adapter or per-dataset configuration, not as evidence that one strict shared-default launcher is required.
- The strict shared-default/paired-launcher experiment from 2026-05-10 is retained as an audit result, not the current required pipeline.

Training path:

```text
scripts/train_mil_cond_*.sh
  -> src/run_train_mil_cond.py
    -> src/anchor_free/train_mil_cond.py
      -> src/helpers/mil_data_helper_cond.py
      -> src/anchor_free/dsnet_af_mil_cond.py
      -> src/evaluate_mil_cond.py
```

Data generation path:

```text
tools/generate_dense_captions_gemini.py
src/make_openclip_features.py
src/make_text_features.py
src/make_video_pseudo_labels.py
src/analyze_shot_utility_formulas.py
```

## Current model/loss summary

- Core model: `DSNetAFMILCond`.
- Core mechanism: visual temporal encoder + text cross-attention + conditioned MIL.
- Current score heads: `single`, `dual`, `residual_dual`.
- Current rank losses: `sparse_pair`, `listwise_utility`, `budgeted_pseudo_summary`, `hybrid_sparse_budget`, `none`.
- Current metrics: F1, Kendall tau-b, Spearman rho, caption coverage.

## Known protocol facts to re-check before changing

- Current split YAML files may not include explicit `val_keys`; current loader may split `train_keys` into train/val by seed.
- Current canonical scripts use `splits/summe.yml` and `splits/tvsum.yml`.
- Augmented/transfer split files may contain mixed datasets; current training code may reject mixed train/val/test dataset names.
- Earlier review found two offline diagnostic scripts may unpack `VideoDatasetMILCond.__getitem__` using an outdated 14-field tuple while the dataset returns 16 fields. Re-check before running or editing:
  - `src/analyze_shot_utility_formulas.py`
  - `src/analyze_budgeted_pseudo_summary_teacher.py`

## Current best trusted results

Fill only from actual logs. Do not infer.

| Dataset | Split mode | Command/tag | Selection metric | F1 | Kendall | Spearman | Seed(s) | Source log |
|---|---|---|---|---:|---:|---:|---|---|
| SumMe | canonical | previous mainline phase1_default | validation F1 | 0.4230±0.0636 | 0.0295±0.0634 | 0.0385±0.0867 | 19500 | remote tmux `chim_MMIL` prior run |
| TVSum | canonical | previous mainline `semantic_plus_rep` | validation F1 | 0.6050±0.0306 | 0.1659±0.0663 | 0.2390±0.0998 | 12345 | remote tmux `chim_MMIL` prior run |

Historical note: the table above contains best per-dataset canonical results. They are valid per-dataset baselines as long as the paper clearly states the dataset adapter/defaults used and does not pretend that a single strict shared-default command produced both rows.

## Strict Shared-Default Audit

| Dataset | Split mode | Command/tag | Selection metric | F1 | Kendall | Spearman | Seed(s) | Source log |
|---|---|---|---|---:|---:|---:|---|---|
| SumMe | canonical unified | `unified_strict_phase1_default_formal_seed19500_summe` | validation F1 | 0.4230+/-0.0636 | 0.0295+/-0.0634 | 0.0385+/-0.0867 | 19500 | `diagnostics/unified_strict_phase1_default_pair_formal.log` |
| TVSum | canonical unified | `unified_strict_phase1_default_formal_seed19500_tvsum` | validation F1 | 0.5939+/-0.0244 | 0.1425+/-0.0439 | 0.2061+/-0.0653 | 19500 | `diagnostics/unified_strict_phase1_default_pair_formal.log` |

Interpretation: this audit over-constrained the protocol by forcing shared defaults and a paired launcher. Keep it for transparency, but do not use it as the required current baseline.

## Recent verified runs

- Remote operations were performed through tmux session `chim_MMIL` in `/data01/chim/code/MMIL_D` with `MMIL_env`.
- `MMIL_env` was upgraded from Python 3.7.12 to Python 3.8.20 so that SciPy 1.10.1 and ORTools' `ortools.algorithms.python.knapsack_solver` API can coexist. Backup: `/data01/chim/code/MMIL_D/diagnostics/env/MMIL_env_before_py38_20260508_184726.yml`.
- Installed and verified in `MMIL_env`: `torch==2.0.1+cu118` with CUDA available, `h5py==3.11.0`, `ortools==9.12.4544`, `PyYAML==6.0.1`, `tqdm==4.67.1`, `tensorboardX==2.6.2.2`, `scikit-learn==1.3.2`.
- Verified no diff in `src/helpers/vsumm_helper.py` before/after the dependency fix; do not edit this file for the current task.
- Added optional SumMe asset path plumbing on remote:
  - `src/run_train_mil_cond.py`: `--text-feature-path`, `--structured-caption-path`.
  - `src/anchor_free/train_mil_cond.py`: passes/logs explicit paths.
  - `src/helpers/mil_data_helper_cond.py`: accepts explicit text feature and structured caption paths for single-dataset runs.
  - `scripts/train_mil_cond_summe_tagr.sh`: forwards `TEXT_FEATURE_PATH`, `STRUCTURED_CAPTION_PATH`, `SHOT_UTILITY_PATH`.
- SumMe v3 smoke, tag `summe_v3_smoke_phase1_default_mmilenv_py38_seed19500`, 1 split / 1 epoch: F1 0.4418, Kendall 0.0003, Spearman 0.0044, coverage 0.9800.
- SumMe v3 formal, tag `summe_v3_budget_dual_phase1_default_mmilenv_py38_seed19500`, 5 splits / 100 epochs: F1 0.4063±0.0302, Kendall -0.0295±0.0713, Spearman -0.0401±0.0973, coverage 0.9800±0.0219.
- TVSum smoke, tag `tvsum_smoke_mmilenv_py38_default_seed19500`, 1 split / 1 epoch: F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000. The new optional path plumbing leaves TVSum default paths as `None`.

Additional 2026-05-09 verified runs and diagnostics:

- Added remote CLI-gated diagnostic/formula support for SumMe v3 caption-summary-prior components in `src/helpers/shot_utility_helper.py`, `src/analyze_shot_utility_formulas.py`, and `src/analyze_budgeted_pseudo_summary_teacher.py`; `src/helpers/vsumm_helper.py` was not changed.
- SumMe v3 diagnostics:
  - `diagnostics/summe_v3_mgs_formula_ablation.json`: validation-ranked utility correlation favored existing `rep_x_anti_redundancy`; best new caption-prior formula was `caption_mgs_rank_safe`, only slightly above `phase1_default` by utility rank.
  - `diagnostics/summe_v3_mgs_budget_teacher.json`: `phase1_default` had best validation pseudo-F1 0.4796; `caption_mgs_rank_safe` had lower pseudo-F1 0.4749 but higher binary-selection Kendall 0.2042 vs 0.1767.
- SumMe v3 caption-prior smoke, tag `summe_v3_mgs_rank_safe_smoke_mmilenv_py38_seed19500`, 1 split / 1 epoch: F1 0.4076, Kendall -0.0039, Spearman -0.0009, coverage 0.9800. Reject; it did not improve over v3 `phase1_default` smoke.
- SumMe v3 CTVSUM-like formula smoke, tag `summe_v3_rep_x_anti_redundancy_smoke_mmilenv_py38_seed19500`, 1 split / 1 epoch: F1 0.4418, Kendall -0.0282, Spearman -0.0359, coverage 0.9800. Reject; F1 matched v3 smoke but rank worsened.
- SumMe v3 hybrid loss smoke, tag `summe_v3_hybrid_sparse_budget_smoke_mmilenv_py38_seed19500`, 1 split / 1 epoch: F1 0.4418, Kendall -0.0016, Spearman 0.0012, coverage 0.9800.
- SumMe v3 hybrid loss formal, tag `summe_v3_hybrid_sparse_budget_mmilenv_py38_seed19500`, 5 splits / 100 epochs: F1 0.3973卤0.0471, Kendall -0.0134卤0.0627, Spearman -0.0186卤0.0860, coverage 0.9800卤0.0219. Reject; all three headline metrics remain below the trusted SumMe baseline.
- TVSum smoke after formula/diagnostic patch, tag `tvsum_smoke_after_mgs_diag_patch_mmilenv_py38_seed19500`, 1 split / 1 epoch: F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000. Default TVSum behavior remains unchanged.

Additional 2026-05-09 checkpoint-selection audit:

- Tested CLI-gated validation checkpoint selection `f1_rank = validation_F1 + 0.25 * mean(validation_Kendall, validation_Spearman)` on remote `chim_MMIL`.
- SumMe smoke, tag `summe_v3_f1_rank_select_smoke_mmilenv_py38_seed19500_w025`, 1 split / 1 epoch: F1 0.4418, Kendall 0.0003, Spearman 0.0044, coverage 0.9800.
- SumMe formal, tag `summe_v3_f1_rank_select_mmilenv_py38_seed19500_w025`, 5 splits / 100 epochs: F1 0.3923+/-0.0418, Kendall -0.0302+/-0.0585, Spearman -0.0404+/-0.0804, coverage 0.9800+/-0.0219.
- TVSum smoke with the temporary selection patch, tag `tvsum_smoke_after_f1_rank_select_patch_mmilenv_py38_seed19500`, 1 split / 1 epoch: F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000.
- Verdict: reject `f1_rank` selection; it worsened SumMe formal results and did not solve the human-preference localization gap.
- Rollback completed on remote. `checkpoint_selection`, `f1_rank`, and `selection_rank_weight` code paths were removed. Post-rollback smokes passed:
  - SumMe tag `summe_v3_after_f1_rank_rollback_smoke_mmilenv_py38_seed19500`: F1 0.4418, Kendall 0.0003, Spearman 0.0044.
  - TVSum tag `tvsum_after_f1_rank_rollback_smoke_mmilenv_py38_seed19500`: F1 0.6102, Kendall 0.0539, Spearman 0.0835.

Additional 2026-05-09 Preference-Distilled MMIL audit:

- Implemented a CLI-gated SumMe preference teacher branch on remote `/data01/chim/code/MMIL_D`; `src/helpers/vsumm_helper.py` was not modified.
- New remote files:
  - `src/helpers/preference_teacher_helper.py`
  - `src/make_llm_preference_teacher.py`
  - `src/analyze_llm_preference_teacher.py`
- Modified remote training entry/loss/script files:
  - `src/run_train_mil_cond.py`
  - `src/anchor_free/train_mil_cond.py`
  - `scripts/train_mil_cond_summe_tagr.sh`
- LLM model choice: `gemini-3.1-pro-preview`. `gemini-3.1-flash-preview` failed a minimal upstream request; `gemini-3.1-pro-preview` and `gemini-3.1-flash-lite-preview` worked, and pro was selected for structured multi-perspective preference scoring.
- Dependency/API check: `openai` and `ortools` are installed in `MMIL_env`; the API key was present in the remote environment and was verified only in masked form.
- Teacher generation completed: `pseudo_labels/summe/llm_preference_teacher_v1.npy`, 25 records, 0 failures. The builder uses LLM `perspective_scores[K,S]`, then creates `summary_masks[K,S]` with `nfps`, 15 percent budget, and knapsack. It does not let the LLM directly decide final masks.
- Label-leakage check passed for teacher construction: `grep -R "gtscore\|user_summary" src/make_llm_preference_teacher.py src/helpers/preference_teacher_helper.py` returned no hits.
- Teacher diagnostic on validation passed the planned threshold and beat baseline teacher on all three metrics:
  - LLM teacher: F1 0.5489, Kendall 0.1722, Spearman 0.2200, budget ratio 0.1356.
  - Baseline teacher: F1 0.5248, Kendall 0.0784, Spearman 0.1075.
  - Deltas: +0.0241 F1, +0.0938 Kendall, +0.1125 Spearman.
- SumMe preference-distill smoke, tag `summe_pref_distill_smoke_v1_mmilenv_py38_seed19500`, 1 split / 1 epoch: F1 0.4271, Kendall 0.0060, Spearman 0.0124, coverage 0.9800.
- SumMe preference-distill formal, tag `summe_pref_distill_formal_v1_mmilenv_py38_seed19500`, 5 splits / 100 epochs: F1 0.3969+/-0.0337, Kendall 0.0010+/-0.0370, Spearman 0.0010+/-0.0516, coverage 0.9800+/-0.0219.
- Verdict: reject for mainline. The offline teacher is stronger than the previous pseudo teacher, but the current training objective/checkpoint path does not convert that teacher advantage into SumMe test improvement. It is below the trusted SumMe baseline F1 0.4230, Kendall 0.0295, Spearman 0.0385.
- Rollback status: do not set `RANK_LOSS=preference_distill` or `PREFERENCE_TEACHER_PATH` for mainline runs. The default SumMe/TVSum scripts still use the existing mainline unless those env vars are explicitly supplied.
- SumMe post-rejection default smoke, tag `summe_post_pref_distill_default_smoke_mmilenv_py38_seed19500`, 1 split / 1 epoch: default `rank_loss=budgeted_pseudo_summary`, preference path `None`, F1 0.4098, Kendall 0.0031, Spearman 0.0077, coverage 0.6400. This verifies the rollback/default path is active when preference env vars are unset.
- TVSum post-formal smoke, tag from `/tmp/run_tvsum_smoke.sh`, 1 split / 1 epoch: F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000. TVSum default path remains unchanged.

Additional 2026-05-09 preference transfer diagnosis:

- Diagnosed why `llm_preference_teacher_v1` passed the first teacher gate but failed formal training. The earlier teacher diagnostic used `analyze_llm_preference_teacher.py` default seed 12345, while the SumMe formal run used seed 19500. This meant the teacher gate was evaluated on a different train/val partition than the actual formal experiment.
- Re-ran teacher diagnostics on the formal seed 19500:
  - LLM teacher: F1 0.4348, Kendall 0.0327, Spearman 0.0458.
  - Baseline teacher: F1 0.4389, Kendall 0.0807, Spearman 0.1134.
  - Deltas: -0.0041 F1, -0.0480 Kendall, -0.0676 Spearman.
  - `train_ready=false`; the teacher does not pass the correct validation gate.
- Added a remote defensive patch to `src/analyze_llm_preference_teacher.py`: if `--seed` is omitted, SumMe now defaults to seed 19500 and TVSum to seed 12345; diagnostic JSON now records `seed`, `seed_explicit`, `val_ratio`, and `splits`.
- Compiled `src/analyze_llm_preference_teacher.py` successfully after the patch.
- Ran temporary transfer diagnostic `/tmp/analyze_pref_transfer.py` on formal validation checkpoints and wrote:
  - `diagnostics/summe_pref_distill_transfer_val_v1.json`
  - `diagnostics/summe_pref_distill_transfer_val_v1.csv`
- Transfer diagnostic summary on formal validation:
  - `best_f1` checkpoint: model F1 0.4409, Tau 0.0783, Rho 0.1056; model-teacher shot Tau 0.0546; pair accuracy 0.5590.
  - `max_kendall` checkpoint: model F1 0.3949, Tau 0.1235, Rho 0.1650; model-teacher shot Tau 0.0379; pair accuracy 0.5778.
  - `max_spearman` checkpoint: model F1 0.3942, Tau 0.1235, Rho 0.1651; model-teacher shot Tau 0.0363; pair accuracy 0.5757.
- Per-video inspection shows a structural teacher issue: several hard validation videos have `num_positive_shots=0` and `num_pairs=0`, so the intended pairwise main loss is skipped on those videos. Examples include `video_9`, `video_10`, `video_13`, and `video_4`, where the LLM teacher rank deltas against baseline are strongly negative.
- Ran a validation-only non-human blend grid between `llm_preference_teacher_v1` shot scores and baseline `phase1_default` utility on seed 19500. Output: `diagnostics/summe_teacher_blend_grid_seed19500_v1.json`.
  - Best F1 blend: LLM weight 0.75, F1 0.4605, Kendall 0.0278, Spearman 0.0434; fails rank thresholds.
  - Best rank blend: LLM weight 0.15, F1 0.4403, Kendall 0.0886, Spearman 0.1249; improves all three metrics over baseline but fails the absolute F1 threshold 0.45.
  - No blend row satisfies the current teacher `train_ready` gate.

Additional 2026-05-09 adaptive preference teacher audit:

- Literature-guided diagnosis favored language-guided summary priors and diversity/reliability calibration, but validation tests showed that a plain LLM/baseline score blend trades off F1 against rank instead of solving both.
- Added remote/local CLI builder `src/build_adaptive_preference_teacher.py`. It does not read `gtscore` or `user_summary`; it uses source preference-teacher pair count as a non-human reliability proxy:
  - if source `pair_count >= 32`, use high LLM blend weight `0.70`;
  - otherwise use conservative LLM blend weight `0.10`;
  - then regenerate `summary_masks`, `inclusion_prob`, and deterministic pairs through the existing preference-teacher helper and knapsack.
- Validation-only adaptive grid on SumMe seed 19500 found train-ready candidates:
  - selected formula `adapt_pair_count_ge_32_low0.10_high0.70`: F1 0.4726, Kendall 0.1219, Spearman 0.1670.
  - seed-matched baseline teacher: F1 0.4389, Kendall 0.0807, Spearman 0.1134.
- Generated `pseudo_labels/summe/adaptive_preference_teacher_v2.npy`:
  - 25 videos, 8 high-weight videos, 17 low-weight videos.
  - mean output pair count 76.08, minimum output pair count 6, fixing the zero-pair issue from the first LLM teacher.
- Teacher diagnostic passed on formal seed 19500:
  - `diagnostics/summe_adaptive_preference_teacher_v2_val_seed19500.json`
  - teacher F1 0.4726, Kendall 0.1219, Spearman 0.1670.
  - deltas vs baseline: +0.0336 F1, +0.0412 Kendall, +0.0536 Spearman.
- SumMe smoke with `RANK_LOSS=preference_distill` and `adaptive_preference_teacher_v2`:
  - tag `summe_pref_distill_adaptive_v2_smoke_mmilenv_py38_seed19500`
  - F1 0.4417, Kendall 0.0150, Spearman 0.0231, coverage 0.9800.
- SumMe formal with `RANK_LOSS=preference_distill` and `adaptive_preference_teacher_v2` failed:
  - tag `summe_pref_distill_adaptive_v2_formal_mmilenv_py38_seed19500`
  - split results:
    - split 1: F1 0.4704, Kendall 0.0754, Spearman 0.1068.
    - split 2: F1 0.4025, Kendall 0.0429, Spearman 0.0595.
    - split 3: F1 0.2980, Kendall -0.1447, Spearman -0.1974.
    - split 4: F1 0.3397, Kendall -0.1149, Spearman -0.1578.
    - split 5: F1 0.3553, Kendall -0.0641, Spearman -0.0895.
  - final: F1 0.3732+/-0.0590, Kendall -0.0411+/-0.0864, Spearman -0.0557+/-0.1194.
  - Verdict: reject for mainline. The teacher diagnostic improves, but the current training/checkpoint path does not transfer it; do not set `RANK_LOSS=preference_distill` or `PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy` for mainline runs.
- TVSum smoke after adding the adaptive builder:
  - tag `tvsum_smoke_after_adaptive_pref_teacher_v2_mmilenv_py38_seed12345`
  - default TVSum path still uses `budgeted_pseudo_summary`, preference path `None`, F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000.

Additional 2026-05-10 teacher-rank selector rejection:

- Tested a temporary CLI-gated validation checkpoint selector `teacher_rank = validation_F1 + 0.25 * mean(validation_Kendall, validation_Spearman) + 0.25 * model-teacher shot-rank agreement` with `RANK_LOSS=preference_distill` and `PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy`.
- This selector used only validation metrics and non-human teacher agreement; test metrics were not used for selection, and training losses still did not use `gtscore` or `user_summary`.
- SumMe smoke, tag `summe_pref_distill_adaptive_v2_teacher_rank_select_smoke_seed19500`: F1 0.4417, Kendall 0.0150, Spearman 0.0231, coverage 0.9800.
- SumMe formal, tag `summe_pref_distill_adaptive_v2_teacher_rank_select_formal_seed19500`, 5 splits:
  - split 1: F1 0.4417, Kendall 0.0308, Spearman 0.0457.
  - split 2: F1 0.3916, Kendall 0.0549, Spearman 0.0774.
  - split 3: F1 0.2980, Kendall -0.1447, Spearman -0.1974.
  - split 4: F1 0.3514, Kendall -0.1215, Spearman -0.1678.
  - split 5: F1 0.3553, Kendall -0.0686, Spearman -0.0938.
  - final: F1 0.3676+/-0.0476, Kendall -0.0498+/-0.0800, Spearman -0.0672+/-0.1109, coverage 0.9800+/-0.0219.
- Verdict: reject. Teacher-aware checkpoint selection is also not enough; the core failure is that the current preference-distill training dynamics invert or erase the teacher/human ranking on hard SumMe folds.
- Rollback completed: removed `CHECKPOINT_SELECTION`, `SELECTION_RANK_WEIGHT`, `SELECTION_TEACHER_WEIGHT`, `checkpoint_selection`, `f1_rank`, and `teacher_rank` plumbing from `scripts/train_mil_cond_summe_tagr.sh`, `src/run_train_mil_cond.py`, and `src/anchor_free/train_mil_cond.py`.
- Remote compile passed after rollback: `/data01/anaconda/envs/MMIL_env/bin/python -m py_compile src/run_train_mil_cond.py src/anchor_free/train_mil_cond.py`.
- SumMe default rollback smoke, tag `summe_after_teacher_rank_rollback_smoke_seed19500`: default `rank_loss=budgeted_pseudo_summary`, preference path `None`, F1 0.4098, Kendall 0.0031, Spearman 0.0077, coverage 0.6400.
- TVSum default rollback smoke, tag `tvsum_after_teacher_rank_rollback_smoke_seed12345`: default `rank_loss=budgeted_pseudo_summary`, preference path `None`, F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000.

Additional 2026-05-10 protocol correction and rollback:

- Corrected the earlier over-interpretation of "unified experiment protocol." The required alignment is shared method/backbone/training logic/input schema/split policy/budget/summary generation/main loss/data flow, not one launcher or one forced set of defaults.
- Removed the over-constraining scripts locally and remotely:
  - `scripts/mil_cond_unified_defaults.sh`
  - `scripts/train_mil_cond_unified_pair.sh`
- Restored separate dataset launcher scripts:
  - `scripts/train_mil_cond_summe_tagr.sh`
  - `scripts/train_mil_cond_tvsum_tagr.sh`
- Remote syntax check passed in tmux `chim_MMIL`:
  - `bash -n scripts/train_mil_cond_summe_tagr.sh scripts/train_mil_cond_tvsum_tagr.sh`
- Rollback smokes passed:
  - SumMe command: `PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_after_strict_unified_rollback_smoke_seed19500 bash scripts/train_mil_cond_summe_tagr.sh`
  - SumMe result: F1 0.4098, Kendall 0.0031, Spearman 0.0077, coverage 0.6400. The run used `phase1_default`, seed 19500, and no preference teacher.
  - TVSum command: `PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=tvsum_after_strict_unified_rollback_smoke_seed12345 bash scripts/train_mil_cond_tvsum_tagr.sh`
  - TVSum result: F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000. The run used `semantic_plus_rep`, seed 12345, and no preference teacher.
- The strict shared-default formal result remains recorded as an audit, but it is not the required paper-facing baseline.

## Active next action

Paper-facing experiments should use the separate SumMe/TVSum launchers as dataset adapters while preserving the same method-level protocol:

1. SumMe: `bash scripts/train_mil_cond_summe_tagr.sh`.
2. TVSum: `bash scripts/train_mil_cond_tvsum_tagr.sh`.
3. Keep the same training entry, backbone, sampled-frame input contract, H5 schema, summary budget, summary generation flow, and main loss/data-flow definition unless a new method branch explicitly changes them for both datasets.
4. Dataset path, split file, log/result directory, and benchmark aggregation adapter may differ by dataset.
5. If a new formula/loss/teacher changes the method, run SumMe first for the bottleneck and then TVSum smoke/formal impact before promoting it.

Do not promote any of these SumMe branches as mainline:

1. `phase1_default + budgeted_pseudo_summary`: formal run lower than trusted SumMe baseline.
2. `caption_mgs_rank_safe`: caption-prior smoke did not improve F1 or rank.
3. `rep_x_anti_redundancy`: CTVSUM-like smoke matched F1 but worsened rank.
4. `phase1_default + hybrid_sparse_budget` with lower selection/budget weights: formal run still lower than trusted SumMe baseline.
5. `f1_rank` validation checkpoint selection: formal run lower than trusted SumMe baseline and lower than v3 `phase1_default`.
6. `preference_distill` with `llm_preference_teacher_v1`: teacher diagnostics improved, but formal training remained below trusted SumMe baseline.
7. `llm_preference_teacher_v1` after correcting diagnostic seed to SumMe formal seed 19500: correct validation teacher gate fails; do not train or promote this teacher.
8. `adaptive_preference_teacher_v2 + preference_distill`: teacher gate passes, but formal training is below the trusted SumMe baseline; keep as diagnostic/ablation only.
9. `adaptive_preference_teacher_v2 + preference_distill + teacher_rank checkpoint selection`: formal run is still below the trusted SumMe baseline; selector was hard-rolled back.

The next controlled action should not promote the current `preference_distill` training branch. Use the generated teacher only for diagnostics/ablation unless a new training objective passes smoke and formal gates:

1. Keep the current mainline rollback active: no `RANK_LOSS=preference_distill` and no `PREFERENCE_TEACHER_PATH` in normal SumMe runs.
2. Do not run more training with `llm_preference_teacher_v1`; it fails the corrected seed-19500 validation teacher gate.
3. Do not run more training with `adaptive_preference_teacher_v2` under the current `preference_distill` objective/checkpoint path; formal results are below the trusted SumMe baseline.
4. The next controlled change should target the training transfer mechanism itself, not another score-only teacher or checkpoint selector:
   - first run a read-only gradient/score diagnostic for `preference_distill` to verify whether pair/list/inclusion/budget terms push `selection_shot_scores` in conflicting directions on hard SumMe folds;
   - then add at most one CLI-gated rank-preserving objective or architecture change if the diagnostic identifies a concrete failure mode;
   - smoke and formal only if the diagnostic justifies the change.
5. Keep training targets free of `gtscore` / `user_summary`; validation human metrics may be used only for diagnostics/selection, not pseudo-label construction.
6. Keep TVSum defaults unchanged and run TVSum smoke after any code change.

## Last completed action

Remote `MMIL_env` dependency fix completed; SumMe v3 path plumbing validated; MGS/caption-prior, CTVSUM-like formula, hybrid sparse-budget, `f1_rank` validation-selection, `preference_distill`, adaptive preference teacher, and `teacher_rank` checkpoint-selection branches were tested and rejected for mainline. The `teacher_rank` selector was hard-rolled back. After the user's protocol correction, the over-constrained shared-default/paired-launcher scheme was rolled back. Separate SumMe/TVSum launchers are restored as dataset adapters, and both smokes passed. The next useful work is a training-transfer diagnostic or ablation that preserves method-level protocol alignment, not another score-only teacher or selector.
