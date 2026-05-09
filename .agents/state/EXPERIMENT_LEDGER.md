# MMIL_D Experiment Ledger

Append one row after each experiment. Do not delete failed runs.

| Date | ID | Dataset | Split | Seed(s) | Change | CLI flags | Selection rule | F1 | Kendall | Spearman | Compared baseline | Verdict | Log path |
|---|---|---|---|---|---|---|---|---:|---:|---:|---|---|---|
| 2026-05-08 | scaffold | n/a | n/a | n/a | Installed Codex skill/state scaffold | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| 2026-05-09 | env_mmil_py38_ortools | n/a | n/a | n/a | Upgraded remote `MMIL_env` to Python 3.8.20 and installed ORTools new API stack | n/a | n/a | n/a | n/a | n/a | n/a | Pass: `ortools.algorithms.python.knapsack_solver`, SciPy `.statistic`, Torch CUDA, h5py imports verified | `/data01/chim/code/MMIL_D/diagnostics/env/MMIL_env_before_py38_20260508_184726.yml` |
| 2026-05-09 | summe_v3_smoke_phase1_default_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | Use v3 SumMe text features, structured captions, and shot utility through explicit path args | `MAX_SPLITS=1 MAX_EPOCH=1 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default` | validation F1 | 0.4418 | 0.0003 | 0.0044 | previous SumMe mainline 0.4230 / 0.0295 / 0.0385 | Smoke pass; coverage improves but rank not improved in 1 epoch | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_smoke_phase1_default_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_v3_budget_dual_phase1_default_mmilenv_py38_seed19500 | SumMe | canonical 5 splits | 19500 | Formal v3 asset path experiment with current budgeted pseudo-summary mainline | `MAX_EPOCH=100 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default` | validation F1 | 0.4063±0.0302 | -0.0295±0.0713 | -0.0401±0.0973 | previous SumMe mainline 0.4230±0.0636 / 0.0295±0.0634 / 0.0385±0.0867 | Reject: coverage improved to 0.9800±0.0219, but all three headline metrics worsened | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_budget_dual_phase1_default_mmilenv_py38_seed19500` |
| 2026-05-09 | tvsum_smoke_mmilenv_py38_default_seed19500 | TVSum | canonical 1 split smoke | 12345 | Check default TVSum path behavior after optional SumMe path plumbing and env fix | `MAX_SPLITS=1 MAX_EPOCH=1` | validation F1 | 0.6102 | 0.0539 | 0.0835 | previous TVSum mainline 0.6050±0.0306 / 0.1659±0.0663 / 0.2390±0.0998 | Smoke pass; default paths remain unset and run is not broken | `/data01/chim/code/MMIL_D/models/mil_cond/tvsum_smoke_mmilenv_py38_default_seed19500` |

| 2026-05-09 | summe_v3_mgs_formula_diagnostics | SumMe | canonical diagnostics | 19500 | Paper-driven MGS/CTVSUM diagnostic formulas | `shot_utility_v3 + text_summe_v3 + structured_captions_v3; formulas include caption_mgs*` | validation diagnostics only | n/a | n/a | n/a | SumMe v3 phase1 teacher diagnostics | Mixed: `phase1_default` best pseudo-F1 0.4796; `caption_mgs_rank_safe` improved binary-selection Kendall but not pseudo-F1 | `/data01/chim/code/MMIL_D/diagnostics/summe_v3_mgs_formula_ablation.json`; `/data01/chim/code/MMIL_D/diagnostics/summe_v3_mgs_budget_teacher.json` |
| 2026-05-09 | summe_v3_mgs_rank_safe_smoke_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | Training-free-language-guided caption prior formula from existing v3 local/global caption similarity | `MAX_SPLITS=1 MAX_EPOCH=1 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=caption_mgs_rank_safe` | validation F1 | 0.4076 | -0.0039 | -0.0009 | v3 phase1 smoke 0.4418 / 0.0003 / 0.0044 | Reject: no smoke improvement; rollback to previous mainline/default formula | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_mgs_rank_safe_smoke_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_v3_rep_x_anti_redundancy_smoke_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | CTVSUM-like representativeness x anti-redundancy utility formula | `MAX_SPLITS=1 MAX_EPOCH=1 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=rep_x_anti_redundancy` | validation F1 | 0.4418 | -0.0282 | -0.0359 | v3 phase1 smoke 0.4418 / 0.0003 / 0.0044 | Reject: F1 matched but rank worsened | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_rep_x_anti_redundancy_smoke_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_v3_hybrid_sparse_budget_smoke_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | Reduce binary pseudo-summary pressure with `hybrid_sparse_budget` and lower weights | `MAX_SPLITS=1 MAX_EPOCH=1 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default RANK_LOSS=hybrid_sparse_budget LAMBDA_SELECT=0.1 LAMBDA_BUDGET=0.02` | validation F1 | 0.4418 | -0.0016 | 0.0012 | v3 phase1 smoke 0.4418 / 0.0003 / 0.0044 | Smoke neutral enough to run formal, but not an improvement by itself | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_hybrid_sparse_budget_smoke_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_v3_hybrid_sparse_budget_mmilenv_py38_seed19500 | SumMe | canonical 5 splits | 19500 | Formal hybrid sparse-budget run with lower pseudo-summary weights | `MAX_EPOCH=100 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default RANK_LOSS=hybrid_sparse_budget LAMBDA_SELECT=0.1 LAMBDA_BUDGET=0.02` | validation F1 | 0.3973卤0.0471 | -0.0134卤0.0627 | -0.0186卤0.0860 | trusted SumMe baseline 0.4230 / 0.0295 / 0.0385 | Reject: below trusted SumMe baseline on all three headline metrics | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_hybrid_sparse_budget_mmilenv_py38_seed19500` |
| 2026-05-09 | tvsum_smoke_after_mgs_diag_patch_mmilenv_py38_seed19500 | TVSum | canonical 1 split smoke | 12345 | Confirm TVSum default path after formula/diagnostic patch | `MAX_SPLITS=1 MAX_EPOCH=1` | validation F1 | 0.6102 | 0.0539 | 0.0835 | prior TVSum smoke 0.6102 / 0.0539 / 0.0835 | Pass: default paths and metrics unchanged | `/data01/chim/code/MMIL_D/models/mil_cond/tvsum_smoke_after_mgs_diag_patch_mmilenv_py38_seed19500` |

| 2026-05-09 | summe_v3_f1_rank_select_smoke_mmilenv_py38_seed19500_w025 | SumMe | canonical 1 split smoke | 19500 | CLI-gated validation checkpoint selection using F1 plus rank term | `MAX_SPLITS=1 MAX_EPOCH=1 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default CHECKPOINT_SELECTION=f1_rank SELECTION_RANK_WEIGHT=0.25` | validation F1 + 0.25 mean rank | 0.4418 | 0.0003 | 0.0044 | v3 phase1 smoke 0.4418 / 0.0003 / 0.0044 | Smoke pass only; run formal because code path works | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_f1_rank_select_smoke_mmilenv_py38_seed19500_w025` |
| 2026-05-09 | summe_v3_f1_rank_select_mmilenv_py38_seed19500_w025 | SumMe | canonical 5 splits | 19500 | Formal validation checkpoint selection using F1 plus rank term | `MAX_EPOCH=100 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default CHECKPOINT_SELECTION=f1_rank SELECTION_RANK_WEIGHT=0.25` | validation F1 + 0.25 mean rank | 0.3923+/-0.0418 | -0.0302+/-0.0585 | -0.0404+/-0.0804 | trusted SumMe baseline 0.4230 / 0.0295 / 0.0385 | Reject and rollback: checkpoint selection cannot repair the teacher-human mismatch | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_f1_rank_select_mmilenv_py38_seed19500_w025` |
| 2026-05-09 | tvsum_smoke_after_f1_rank_select_patch_mmilenv_py38_seed19500 | TVSum | canonical 1 split smoke | 12345 | Confirm TVSum default path under temporary checkpoint-selection patch | `MAX_SPLITS=1 MAX_EPOCH=1` | validation F1 | 0.6102 | 0.0539 | 0.0835 | prior TVSum smoke 0.6102 / 0.0539 / 0.0835 | Pass: TVSum default behavior unchanged under the temporary patch | `/data01/chim/code/MMIL_D/models/mil_cond/tvsum_smoke_after_f1_rank_select_patch_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_v3_after_f1_rank_rollback_smoke_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | Verify SumMe path after rolling back rejected checkpoint-selection module | `MAX_SPLITS=1 MAX_EPOCH=1 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default` | validation F1 | 0.4418 | 0.0003 | 0.0044 | v3 phase1 smoke 0.4418 / 0.0003 / 0.0044 | Pass: rollback restored mainline runtime behavior | `/data01/chim/code/MMIL_D/models/mil_cond/summe_v3_after_f1_rank_rollback_smoke_mmilenv_py38_seed19500` |
| 2026-05-09 | tvsum_after_f1_rank_rollback_smoke_mmilenv_py38_seed19500 | TVSum | canonical 1 split smoke | 12345 | Verify TVSum path after rolling back rejected checkpoint-selection module | `MAX_SPLITS=1 MAX_EPOCH=1` | validation F1 | 0.6102 | 0.0539 | 0.0835 | prior TVSum smoke 0.6102 / 0.0539 / 0.0835 | Pass: rollback did not affect TVSum default behavior | `/data01/chim/code/MMIL_D/models/mil_cond/tvsum_after_f1_rank_rollback_smoke_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_llm_preference_teacher_v1_val | SumMe | canonical validation diagnostic | 19500 | Build and diagnose LLM multi-perspective preference teacher; masks generated by knapsack, not directly by LLM | `src/make_llm_preference_teacher.py --num-perspectives 7 --summary-budget 0.15 --max-pairs-per-video 96 --pair-seed 19500`; `src/analyze_llm_preference_teacher.py --selection-part val` | validation diagnostic only | 0.5489 | 0.1722 | 0.2200 | baseline teacher 0.5248 / 0.0784 / 0.1075 | Pass teacher gate: all absolute thresholds met and all three metrics beat baseline teacher | `/data01/chim/code/MMIL_D/diagnostics/summe_llm_preference_teacher_v1_val.json` |
| 2026-05-09 | summe_pref_distill_smoke_v1_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | Train with CLI-gated `preference_distill` using LLM preference teacher | `MAX_SPLITS=1 MAX_EPOCH=1 RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/llm_preference_teacher_v1.npy TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json` | validation F1 | 0.4271 | 0.0060 | 0.0124 | trusted SumMe baseline 0.4230 / 0.0295 / 0.0385 | Smoke runs but rank remains weak; formal required before any promotion | `/data01/chim/code/MMIL_D/models/mil_cond/summe_pref_distill_smoke_v1_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_pref_distill_formal_v1_mmilenv_py38_seed19500 | SumMe | canonical 5 splits | 19500 | Formal `preference_distill` training with `llm_preference_teacher_v1` | `MAX_EPOCH=100 RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/llm_preference_teacher_v1.npy TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json` | validation F1 | 0.3969+/-0.0337 | 0.0010+/-0.0370 | 0.0010+/-0.0516 | trusted SumMe baseline 0.4230 / 0.0295 / 0.0385 | Reject: offline teacher improves, but training transfer fails; do not promote preference_distill mainline | `/data01/chim/code/MMIL_D/models/mil_cond/summe_pref_distill_formal_v1_mmilenv_py38_seed19500` |
| 2026-05-09 | summe_post_pref_distill_default_smoke_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | Verify rollback/default SumMe path after rejected preference-distill formal | `MAX_SPLITS=1 MAX_EPOCH=1 DEVICE=cuda RUN_TAG=summe_post_pref_distill_default_smoke_mmilenv_py38_seed19500 bash scripts/train_mil_cond_summe_tagr.sh` | validation F1 | 0.4098 | 0.0031 | 0.0077 | prior default SumMe smoke path | Pass: default path uses `budgeted_pseudo_summary`, preference path `None`, and `shot_utility.npy` | `/data01/chim/code/MMIL_D/models/mil_cond/summe_post_pref_distill_default_smoke_mmilenv_py38_seed19500` |
| 2026-05-09 | tvsum_post_pref_distill_formal_smoke_mmilenv_py38_seed12345 | TVSum | canonical 1 split smoke | 12345 | Confirm TVSum default behavior after preference-distill code path and rejected formal | `MAX_SPLITS=1 MAX_EPOCH=1 DEVICE=cuda bash scripts/train_mil_cond_tvsum_tagr.sh` | validation F1 | 0.6102 | 0.0539 | 0.0835 | prior TVSum smoke 0.6102 / 0.0539 / 0.0835 | Pass: default TVSum remains `budgeted_pseudo_summary`; preference args parsed but unused | `/data01/chim/code/MMIL_D/models/mil_cond/tvsum_smoke_mmilenv_py38_default_seed19500` |
| 2026-05-09 | summe_llm_preference_teacher_v1_val_seed19500 | SumMe | canonical validation diagnostic | 19500 | Re-run LLM preference teacher gate on the same split seed used by formal SumMe training | `src/analyze_llm_preference_teacher.py --dataset summe --splits splits/summe.yml --teacher-path pseudo_labels/summe/llm_preference_teacher_v1.npy --baseline-shot-utility-path pseudo_labels/summe/shot_utility_v3.npy --baseline-formula phase1_default --selection-part val --seed 19500` | validation diagnostic only | 0.4348 | 0.0327 | 0.0458 | seed-matched baseline teacher 0.4389 / 0.0807 / 0.1134 | Reject: corrected validation gate fails; previous pass used mismatched seed 12345 | `/data01/chim/code/MMIL_D/diagnostics/summe_llm_preference_teacher_v1_val_seed19500.json` |
| 2026-05-09 | summe_pref_distill_transfer_val_v1 | SumMe | canonical validation diagnostic | 19500 | Diagnose teacher-to-training transfer on saved preference-distill checkpoints | temporary `/tmp/analyze_pref_transfer.py --parts val --model-dir models/mil_cond/summe_pref_distill_formal_v1_mmilenv_py38_seed19500` | validation diagnostic only | 0.4409 best-F1 checkpoint | 0.0783 best-F1 checkpoint | 0.1056 best-F1 checkpoint | teacher seed-19500 F1 0.4348 / 0.0327 / 0.0458 | Diagnostic: model can improve validation rank over weak teacher, but teacher gate itself fails and several videos have zero positive pairs | `/data01/chim/code/MMIL_D/diagnostics/summe_pref_distill_transfer_val_v1.json` |
| 2026-05-09 | summe_teacher_blend_grid_seed19500_v1 | SumMe | canonical validation diagnostic | 19500 | Builder-only blend grid between LLM preference teacher scores and baseline phase1 utility | `llm_weight in {0.00..1.00 step 0.05}; score=normalize(llm_weight*llm + (1-llm_weight)*baseline)` | validation diagnostic only | 0.4403 best-rank blend | 0.0886 best-rank blend | 0.1249 best-rank blend | seed-matched baseline teacher 0.4389 / 0.0807 / 0.1134 | Reject for training gate: best rank blend improves all three over baseline but F1 remains below 0.45; no train-ready row | `/data01/chim/code/MMIL_D/diagnostics/summe_teacher_blend_grid_seed19500_v1.json` |
| 2026-05-09 | summe_teacher_adaptive_blend_seed19500_v1 | SumMe | canonical validation diagnostic | 19500 | Validation-only adaptive blend grid using source preference pair count as reliability proxy | `adapt_pair_count_ge_32_low0.10_high0.70` | validation diagnostic only | 0.4726 | 0.1219 | 0.1670 | seed-matched baseline teacher 0.4389 / 0.0807 / 0.1134 | Pass teacher gate: all absolute thresholds met and all three metrics improve over baseline; allowed for smoke only | `/data01/chim/code/MMIL_D/diagnostics/summe_teacher_adaptive_blend_seed19500_v1.json` |
| 2026-05-09 | summe_adaptive_preference_teacher_v2_val_seed19500 | SumMe | canonical validation diagnostic | 19500 | Build adaptive preference teacher with CLI builder and diagnose same seed | `src/build_adaptive_preference_teacher.py --pair-count-threshold 32 --low-llm-weight 0.10 --high-llm-weight 0.70`; `src/analyze_llm_preference_teacher.py --seed 19500` | validation diagnostic only | 0.4726 | 0.1219 | 0.1670 | seed-matched baseline teacher 0.4389 / 0.0807 / 0.1134 | Pass teacher gate; source zero-pair issue fixed in output teacher, min output pairs 6 | `/data01/chim/code/MMIL_D/diagnostics/summe_adaptive_preference_teacher_v2_val_seed19500.json` |
| 2026-05-09 | summe_pref_distill_adaptive_v2_smoke_mmilenv_py38_seed19500 | SumMe | canonical 1 split smoke | 19500 | Train `preference_distill` with adaptive teacher v2 | `MAX_SPLITS=1 MAX_EPOCH=1 RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy` | validation F1 | 0.4417 | 0.0150 | 0.0231 | v3 phase1 smoke 0.4418 / 0.0003 / 0.0044 | Smoke acceptable for formal: F1 neutral, rank improved over prior smoke, but not enough to promote | `/data01/chim/code/MMIL_D/diagnostics/summe_pref_distill_adaptive_v2_smoke.log` |
| 2026-05-09 | summe_pref_distill_adaptive_v2_formal_mmilenv_py38_seed19500 | SumMe | canonical 5 splits | 19500 | Formal `preference_distill` with adaptive teacher v2 | `RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy` | validation F1 | 0.3732+/-0.0590 | -0.0411+/-0.0864 | -0.0557+/-0.1194 | trusted SumMe baseline 0.4230 / 0.0295 / 0.0385 | Reject: teacher diagnostic does not transfer through current training/checkpoint path; keep as diagnostic/ablation only | `/data01/chim/code/MMIL_D/diagnostics/summe_pref_distill_adaptive_v2_formal.log` |
| 2026-05-09 | tvsum_smoke_after_adaptive_pref_teacher_v2_mmilenv_py38_seed12345 | TVSum | canonical 1 split smoke | 12345 | Confirm TVSum default path after adaptive teacher builder addition | `MAX_SPLITS=1 MAX_EPOCH=1 DEVICE=cuda bash scripts/train_mil_cond_tvsum_tagr.sh` | validation F1 | 0.6102 | 0.0539 | 0.0835 | prior TVSum smoke 0.6102 / 0.0539 / 0.0835 | Pass: TVSum default remains utility-based, preference path None | `/data01/chim/code/MMIL_D/diagnostics/tvsum_smoke_after_adaptive_pref_teacher_v2.log` |
| 2026-05-10 | summe_pref_distill_adaptive_v2_teacher_rank_select_formal_seed19500 | SumMe | canonical 5 splits | 19500 | Test validation-only teacher-aware checkpoint selector on adaptive preference distill | `RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy CHECKPOINT_SELECTION=teacher_rank SELECTION_RANK_WEIGHT=0.25 SELECTION_TEACHER_WEIGHT=0.25` | validation F1 + rank + teacher agreement | 0.3676+/-0.0476 | -0.0498+/-0.0800 | -0.0672+/-0.1109 | trusted SumMe baseline 0.4230 / 0.0295 / 0.0385 | Reject and rollback: selector does not solve hard-fold rank inversion | `/data01/chim/code/MMIL_D/diagnostics/summe_pref_distill_adaptive_v2_teacher_rank_select_formal.log` |
| 2026-05-10 | summe_after_teacher_rank_rollback_smoke_seed19500 | SumMe | canonical 1 split smoke | 19500 | Verify SumMe default path after hard rollback of teacher-rank selector | `MAX_SPLITS=1 MAX_EPOCH=1 DEVICE=cuda RUN_TAG=summe_after_teacher_rank_rollback_smoke_seed19500 bash scripts/train_mil_cond_summe_tagr.sh` | validation F1 | 0.4098 | 0.0031 | 0.0077 | prior default SumMe smoke 0.4098 / 0.0031 / 0.0077 | Pass: default path uses `budgeted_pseudo_summary`, preference path None | `/data01/chim/code/MMIL_D/diagnostics/summe_after_teacher_rank_rollback_smoke.log` |
| 2026-05-10 | tvsum_after_teacher_rank_rollback_smoke_seed12345 | TVSum | canonical 1 split smoke | 12345 | Verify TVSum default path after hard rollback of teacher-rank selector | `MAX_SPLITS=1 MAX_EPOCH=1 DEVICE=cuda RUN_TAG=tvsum_after_teacher_rank_rollback_smoke_seed12345 bash scripts/train_mil_cond_tvsum_tagr.sh` | validation F1 | 0.6102 | 0.0539 | 0.0835 | prior TVSum smoke 0.6102 / 0.0539 / 0.0835 | Pass: TVSum default remains unchanged | `/data01/chim/code/MMIL_D/diagnostics/tvsum_after_teacher_rank_rollback_smoke.log` |
| 2026-05-10 | strict_unified_launcher_rollback | n/a | n/a | n/a | Roll back over-constrained shared-default/paired-launcher interpretation after protocol correction | restore separate `scripts/train_mil_cond_summe_tagr.sh` and `scripts/train_mil_cond_tvsum_tagr.sh`; remove `scripts/mil_cond_unified_defaults.sh` and `scripts/train_mil_cond_unified_pair.sh` | n/a | n/a | n/a | n/a | strict shared-default audit | Pass: method-level protocol alignment is retained; dataset adapters are allowed | remote tmux `chim_MMIL` |
| 2026-05-10 | summe_after_strict_unified_rollback_smoke_seed19500 | SumMe | canonical 1 split smoke | 19500 | Verify SumMe launcher after rollback of strict shared-default scheme | `MAX_SPLITS=1 MAX_EPOCH=1 DEVICE=cuda RUN_TAG=summe_after_strict_unified_rollback_smoke_seed19500 bash scripts/train_mil_cond_summe_tagr.sh` | validation F1 | 0.4098 | 0.0031 | 0.0077 | prior default SumMe smoke 0.4098 / 0.0031 / 0.0077 | Pass: SumMe uses `phase1_default`, seed 19500, no preference teacher | `/data01/chim/code/MMIL_D/diagnostics/summe_after_strict_unified_rollback_smoke.log` |
| 2026-05-10 | tvsum_after_strict_unified_rollback_smoke_seed12345 | TVSum | canonical 1 split smoke | 12345 | Verify TVSum launcher after rollback of strict shared-default scheme | `MAX_SPLITS=1 MAX_EPOCH=1 DEVICE=cuda RUN_TAG=tvsum_after_strict_unified_rollback_smoke_seed12345 bash scripts/train_mil_cond_tvsum_tagr.sh` | validation F1 | 0.6102 | 0.0539 | 0.0835 | prior TVSum smoke 0.6102 / 0.0539 / 0.0835 | Pass: TVSum uses `semantic_plus_rep`, seed 12345, no preference teacher | `/data01/chim/code/MMIL_D/diagnostics/tvsum_after_strict_unified_rollback_smoke.log` |

## Required notes per experiment

```text
Hypothesis:
Files changed:
Why this does not use frame-level human labels for training:
Smoke command:
Formal command:
Rollback command:
Main result:
Failure analysis:
Next decision:
```

## 2026-05-09 notes

Hypothesis:
SumMe v3 dense captions and v3 shot utility would improve SumMe by increasing valid caption coverage and using stronger non-human semantic evidence.

Files changed:
Remote code path only: `src/run_train_mil_cond.py`, `src/anchor_free/train_mil_cond.py`, `src/helpers/mil_data_helper_cond.py`, `scripts/train_mil_cond_summe_tagr.sh`. `src/helpers/vsumm_helper.py` was intentionally not modified.

Why this does not use frame-level human labels for training:
The v3 assets are dense caption/text-feature/shot-utility assets derived from non-human semantic evidence. Training still uses weak/pseudo supervision only; `gtscore` and `user_summary` remain evaluation/validation signals.

Smoke command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_v3_smoke_phase1_default_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default bash scripts/train_mil_cond_summe_tagr.sh`

Formal command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_EPOCH=100 RUN_TAG=summe_v3_budget_dual_phase1_default_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default bash scripts/train_mil_cond_summe_tagr.sh`

Rollback command:
Use the previous default SumMe script without `TEXT_FEATURE_PATH`, `STRUCTURED_CAPTION_PATH`, or `SHOT_UTILITY_PATH`; if needed, revert remote path-plumbing edits in `src/run_train_mil_cond.py`, `src/anchor_free/train_mil_cond.py`, `src/helpers/mil_data_helper_cond.py`, and `scripts/train_mil_cond_summe_tagr.sh`.

Main result:
SumMe v3 formal: F1 0.4063±0.0302, Kendall -0.0295±0.0713, Spearman -0.0401±0.0973, caption coverage 0.9800±0.0219.

Failure analysis:
The v3 assets solved much of the coverage problem but did not solve the ranking problem. Validation traces show F1 can rise while Tau/Rho fall, so `phase1_default + budgeted_pseudo_summary` appears to over-optimize pseudo-summary selection and distort human-score ordering on SumMe. This is consistent with SumMe's small size and stronger sensitivity to shot-level teacher mismatch.

Next decision:
Do not tune on test metrics. Next run should be a CLI-gated SumMe-only experiment that reduces rank damage, for example `hybrid_sparse_budget`, smaller `lambda_budget`/`lambda_select`, or a teacher formula chosen from non-human diagnostics and validated without test-key selection. Keep TVSum defaults unchanged and run TVSum smoke after each code/loss change.

## 2026-05-09 paper-driven diagnostic notes

Hypothesis:
Caption descriptions could be upgraded into a weak summary prior using multi-grained caption saliency, and contrastive/anti-redundancy utilities could better match SumMe human preference than semantic coverage alone.

Files changed:
Remote code path only: `src/helpers/shot_utility_helper.py`, `src/analyze_shot_utility_formulas.py`, `src/analyze_budgeted_pseudo_summary_teacher.py`. `src/helpers/vsumm_helper.py` was intentionally not modified.

Why this does not use frame-level human labels for training:
The added formulas use only existing v3 non-human components (`local_caption_similarity_raw`, `global_caption_similarity_raw`, `caption_change_raw`, `visual_change_raw`, and existing utility components). Human labels were used only in offline diagnostics and validation/test reporting.

Smoke commands:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_v3_mgs_rank_safe_smoke_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=caption_mgs_rank_safe bash scripts/train_mil_cond_summe_tagr.sh`

`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_v3_rep_x_anti_redundancy_smoke_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=rep_x_anti_redundancy bash scripts/train_mil_cond_summe_tagr.sh`

Formal command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_EPOCH=100 RUN_TAG=summe_v3_hybrid_sparse_budget_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default RANK_LOSS=hybrid_sparse_budget LAMBDA_SELECT=0.1 LAMBDA_BUDGET=0.02 bash scripts/train_mil_cond_summe_tagr.sh`

Rollback command:
Use the trusted previous SumMe mainline command without v3 paths, without `caption_mgs*`, and without `RANK_LOSS=hybrid_sparse_budget`. Formula/diagnostic code is CLI-gated; hard rollback is available from `/data01/chim/code/MMIL_D/diagnostics/code_backups/mgs_prior_patch_20260508_195756`.

Main result:
MGS caption-prior smoke and CTVSUM-like formula smoke did not improve SumMe rank. Hybrid sparse-budget formal ended at F1 0.3973卤0.0471, Kendall -0.0134卤0.0627, Spearman -0.0186卤0.0860, below the trusted SumMe baseline.

Failure analysis:
The additional non-human teacher formulas did not solve the human-preference localization gap. Training traces show validation F1 and validation rank diverge sharply: better F1 checkpoints frequently sit in lower or negative rank regions. The current bottleneck is now checkpoint/objective mismatch more than caption coverage or one more handcrafted utility formula.

Next decision:
Do not promote the tested formula/loss branches. Next experiment should be CLI-gated validation checkpoint selection that balances validation F1 and validation rank, while keeping test metrics strictly for reporting and training targets free of human labels.

## 2026-05-09 checkpoint-selection rejection notes

Hypothesis:
Balancing validation F1 with validation Kendall/Spearman during checkpoint selection might reduce SumMe's F1/rank objective mismatch without changing training supervision or pseudo labels.

Files changed:
Temporary remote code path only: `src/anchor_free/train_mil_cond.py`, `src/run_train_mil_cond.py`, `scripts/train_mil_cond_summe_tagr.sh`, `scripts/train_mil_cond_tvsum_tagr.sh`. The rejected code path was rolled back. `src/helpers/vsumm_helper.py` was intentionally not modified.

Why this does not use frame-level human labels for training:
The temporary selector used validation metrics only for checkpoint selection/reporting. Training losses and pseudo labels still did not use `gtscore`, `user_summary`, or human-derived keyshot targets.

Smoke command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_v3_f1_rank_select_smoke_mmilenv_py38_seed19500_w025 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default CHECKPOINT_SELECTION=f1_rank SELECTION_RANK_WEIGHT=0.25 bash scripts/train_mil_cond_summe_tagr.sh`

Formal command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_EPOCH=100 RUN_TAG=summe_v3_f1_rank_select_mmilenv_py38_seed19500_w025 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json SHOT_UTILITY_PATH=pseudo_labels/summe/shot_utility_v3.npy UTILITY_FORMULA=phase1_default CHECKPOINT_SELECTION=f1_rank SELECTION_RANK_WEIGHT=0.25 bash scripts/train_mil_cond_summe_tagr.sh`

Rollback command:
Restore validation-F1 checkpoint selection and remove `CHECKPOINT_SELECTION`, `SELECTION_RANK_WEIGHT`, `checkpoint_selection`, `selection_rank_weight`, and `f1_rank` code paths. Remote rollback backup: `/data01/chim/code/MMIL_D/diagnostics/code_backups/checkpoint_selection_rejected_20260508_212404`.

Main result:
SumMe `f1_rank` formal: F1 0.3923+/-0.0418, Kendall -0.0302+/-0.0585, Spearman -0.0404+/-0.0804, coverage 0.9800+/-0.0219. TVSum smoke under the temporary patch remained unchanged at F1 0.6102, Kendall 0.0539, Spearman 0.0835.

Failure analysis:
The selector chose earlier checkpoints with better validation rank in some folds, but test rank remained unstable and the final F1 dropped. This shows the current bottleneck is not only checkpoint selection; the non-human teacher still does not encode SumMe human preference strongly enough.

Next decision:
Do not promote `f1_rank`. Stop selector-level fixes and build a stronger non-human summary-prior teacher, starting with validation-only teacher diagnostics and then a CLI-gated caption-derived textual summary prior.

## 2026-05-09 preference-distilled MMIL rejection notes

Hypothesis:
Replacing handcrafted SumMe pseudo-summary supervision with a multi-perspective LLM preference teacher would better match SumMe's human-preference saliency while leaving TVSum defaults unchanged.

Files changed:
Remote code path: `src/helpers/preference_teacher_helper.py`, `src/make_llm_preference_teacher.py`, `src/analyze_llm_preference_teacher.py`, `src/run_train_mil_cond.py`, `src/anchor_free/train_mil_cond.py`, `scripts/train_mil_cond_summe_tagr.sh`. `src/helpers/vsumm_helper.py` was intentionally not modified.

Why this does not use frame-level human labels for training:
The teacher builder uses structured captions, H5 shot metadata, LLM preference scores, and knapsack. It does not read `gtscore` or `user_summary`; those are used only in `analyze_llm_preference_teacher.py` for offline diagnostics.

Teacher diagnostic:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python ${PYTHON_BIN} src/analyze_llm_preference_teacher.py --dataset summe --splits splits/summe.yml --teacher-path pseudo_labels/summe/llm_preference_teacher_v1.npy --baseline-shot-utility-path pseudo_labels/summe/shot_utility_v3.npy --baseline-formula phase1_default --selection-part val --summary-budget 0.15 --output-json diagnostics/summe_llm_preference_teacher_v1_val.json --output-csv diagnostics/summe_llm_preference_teacher_v1_val.csv`

Smoke command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_pref_distill_smoke_v1_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/llm_preference_teacher_v1.npy bash scripts/train_mil_cond_summe_tagr.sh`

Formal command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda RUN_TAG=summe_pref_distill_formal_v1_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/llm_preference_teacher_v1.npy bash scripts/train_mil_cond_summe_tagr.sh`

Rollback command:
Use the default scripts without `RANK_LOSS=preference_distill` and without `PREFERENCE_TEACHER_PATH`. The branch is CLI-gated; TVSum defaults remain unchanged.

Main result:
Teacher validation diagnostic passed: F1 0.5489, Kendall 0.1722, Spearman 0.2200 versus baseline teacher 0.5248 / 0.0784 / 0.1075. Training formal failed: SumMe F1 0.3969+/-0.0337, Kendall 0.0010+/-0.0370, Spearman 0.0010+/-0.0516, below the trusted SumMe baseline.

Rollback verification:
SumMe default smoke without preference env vars used `rank_loss=budgeted_pseudo_summary`, `preference path=None`, and default `shot_utility.npy`, producing F1 0.4098, Kendall 0.0031, Spearman 0.0077. TVSum post-formal smoke stayed unchanged at F1 0.6102, Kendall 0.0539, Spearman 0.0835.

Failure analysis:
The teacher construction improved offline alignment, but current training transfer is unstable. Some folds get reasonable F1 while rank collapses or becomes negative, so `selection_shot_scores` trained with the current pair/list/inclusion mixture do not reliably preserve the teacher's human-preference ordering under the existing validation-F1 checkpoint rule.

Corrected diagnosis:
The stronger issue is that the original teacher gate used the wrong validation split seed. `analyze_llm_preference_teacher.py` defaulted to seed 12345, but the SumMe formal command used seed 19500. With seed 19500, `llm_preference_teacher_v1` fails the validation gate and is worse than the baseline teacher on all three diagnostic metrics. The diagnostic script now defaults SumMe to seed 19500 and records seed metadata in JSON.

Next decision:
Do not promote `preference_distill`. Keep `llm_preference_teacher_v1` as a diagnostic asset only. The next safe step is a builder-only teacher ablation that reduces zero-positive/zero-pair videos and then re-runs seed-19500 validation diagnostics before any training.

## 2026-05-09 adaptive preference teacher rejection notes

Hypothesis:
The first LLM teacher failed partly because low-confidence videos had zero or weak preference pairs. A reliability-gated blend could use the source teacher only where it had enough preference pairs, otherwise fall back toward the non-human phase1 teacher.

Files changed:
Added `src/build_adaptive_preference_teacher.py`. Existing training files were not changed in this step. `src/helpers/vsumm_helper.py` was intentionally not modified.

Why this does not use frame-level human labels for training:
The builder uses `llm_preference_teacher_v1`, non-human `shot_utility_v3`, H5 shot metadata, and knapsack. It does not read `gtscore` or `user_summary`; those are used only by diagnostic scripts for validation reporting.

Smoke command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_pref_distill_adaptive_v2_smoke_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy bash scripts/train_mil_cond_summe_tagr.sh`

Formal command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda RUN_TAG=summe_pref_distill_adaptive_v2_formal_mmilenv_py38_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy bash scripts/train_mil_cond_summe_tagr.sh`

Rollback command:
Leave `RANK_LOSS` and `PREFERENCE_TEACHER_PATH` unset for mainline runs. The adaptive builder is not on the default path; hard rollback is removing `src/build_adaptive_preference_teacher.py` and ignoring `pseudo_labels/summe/adaptive_preference_teacher_v2.npy`.

Main result:
Teacher validation gate passed at F1 0.4726, Kendall 0.1219, Spearman 0.1670, but formal training failed at F1 0.3732+/-0.0590, Kendall -0.0411+/-0.0864, Spearman -0.0557+/-0.1194.

Failure analysis:
The adaptive teacher solves a teacher-construction diagnostic and removes zero-pair videos, but the current `preference_distill` objective plus validation-F1 checkpoint selection does not preserve teacher ordering through training. Several folds show validation rank collapsing while loss continues decreasing.

Next decision:
Do not build another score-only teacher immediately. Next work should target teacher-to-training transfer: a CLI-gated teacher-aware validation selector or rank-preserving regularization/early stopping that never uses test metrics and never uses human labels in the training loss.

## 2026-05-10 teacher-rank selector rejection notes

Hypothesis:
A validation-only selector combining validation F1, validation rank, and model-teacher shot-rank agreement might keep the adaptive preference-distill branch from drifting into rank-inverted checkpoints on SumMe.

Files changed:
Temporary remote/local code path: `src/anchor_free/train_mil_cond.py`, `src/run_train_mil_cond.py`, `scripts/train_mil_cond_summe_tagr.sh`. The selector was hard-rolled back after formal failure. `src/helpers/vsumm_helper.py` was not modified.

Why this does not use frame-level human labels for training:
The selector used validation metrics and non-human teacher agreement only for checkpoint selection. Training losses and pseudo labels did not use `gtscore`, `user_summary`, or human-derived keyshot targets.

Smoke command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_pref_distill_adaptive_v2_teacher_rank_select_smoke_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy CHECKPOINT_SELECTION=teacher_rank SELECTION_RANK_WEIGHT=0.25 SELECTION_TEACHER_WEIGHT=0.25 bash scripts/train_mil_cond_summe_tagr.sh`

Formal command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda RUN_TAG=summe_pref_distill_adaptive_v2_teacher_rank_select_formal_seed19500 TEXT_FEATURE_PATH=features/text_summe_v3.h5 STRUCTURED_CAPTION_PATH=captions_raw/summe_dense_captions_structured_v3.json RANK_LOSS=preference_distill PREFERENCE_TEACHER_PATH=pseudo_labels/summe/adaptive_preference_teacher_v2.npy CHECKPOINT_SELECTION=teacher_rank SELECTION_RANK_WEIGHT=0.25 SELECTION_TEACHER_WEIGHT=0.25 bash scripts/train_mil_cond_summe_tagr.sh`

Rollback command:
Remove `CHECKPOINT_SELECTION`, `SELECTION_RANK_WEIGHT`, `SELECTION_TEACHER_WEIGHT`, `checkpoint_selection`, `f1_rank`, and `teacher_rank` paths from `scripts/train_mil_cond_summe_tagr.sh`, `src/run_train_mil_cond.py`, and `src/anchor_free/train_mil_cond.py`; then compile and run SumMe/TVSum default smokes.

Main result:
SumMe formal failed at F1 0.3676+/-0.0476, Kendall -0.0498+/-0.0800, Spearman -0.0672+/-0.1109, below both the trusted SumMe baseline and the previous adaptive preference-distill formal.

Rollback verification:
Remote compile passed. SumMe default rollback smoke produced F1 0.4098, Kendall 0.0031, Spearman 0.0077 with `rank_loss=budgeted_pseudo_summary` and preference path None. TVSum default rollback smoke stayed unchanged at F1 0.6102, Kendall 0.0539, Spearman 0.0835.

Failure analysis:
The selector can pick early checkpoints with better validation agreement, but hard SumMe folds still have negative test rank. This means the bottleneck is not checkpoint selection. The current training objective or representation does not reliably transfer teacher preference into stable `selection_shot_scores`.

Next decision:
Do not add another teacher or selector. Next action should be a read-only training-transfer diagnostic: per-video loss/gradient contribution, teacher rank vs model rank, and shot aggregation behavior on hard folds. Only add a new CLI-gated training branch after that diagnostic identifies the exact rank-destroying term.

## 2026-05-10 strict shared-default SumMe+TVSum audit

Hypothesis:
The previous best SumMe and TVSum results used different dataset adapter defaults. This audit tested whether forcing one shared-default paired launcher was necessary for protocol alignment.

Files changed:
Added `scripts/mil_cond_unified_defaults.sh` and `scripts/train_mil_cond_unified_pair.sh`. Updated `scripts/train_mil_cond_summe_tagr.sh` and `scripts/train_mil_cond_tvsum_tagr.sh` to source the same defaults. `src/helpers/vsumm_helper.py`, `splits/*.yml`, and training Python files were not changed in this step.

Unified protocol:
Both datasets now share `SEED=19500`, `RANK_LOSS=budgeted_pseudo_summary`, `SCORE_HEAD=dual`, `UTILITY_FORMULA=phase1_default`, `SUMMARY_BUDGET=0.15`, `TEXT_COND_NUM=10`, `NUM_FEATURE=768`, `WEIGHT_DECAY=2e-5`, `LAMBDA_ALIGN=1.0`, and `LAMBDA_AUX=2.0`. In strict mode, explicit dataset-only `SHOT_UTILITY_PATH`, `TEXT_FEATURE_PATH`, `STRUCTURED_CAPTION_PATH`, and `PREFERENCE_TEACHER_PATH` overrides are blocked.

Why this does not use frame-level human labels for training:
The run uses the existing non-human `shot_utility.npy` pseudo supervision and validation-F1 checkpoint selection. Training losses and pseudo labels do not use `gtscore`, `user_summary`, or human-derived keyshot targets.

Syntax and guard checks:
`bash -n scripts/mil_cond_unified_defaults.sh scripts/train_mil_cond_summe_tagr.sh scripts/train_mil_cond_tvsum_tagr.sh scripts/train_mil_cond_unified_pair.sh`

`STRICT_UNIFIED_PIPELINE=1 UTILITY_FORMULA=semantic_plus_rep MAX_SPLITS=1 MAX_EPOCH=1 bash scripts/train_mil_cond_summe_tagr.sh` exited before training with code 2, confirming dataset-only formula drift is blocked.

Smoke command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 PAIR_TAG=unified_strict_phase1_default_smoke_seed19500 bash scripts/train_mil_cond_unified_pair.sh`

Smoke result:
Log `diagnostics/unified_strict_phase1_default_pair_smoke.log`. SumMe: F1 0.4098, Kendall 0.0031, Spearman 0.0077, coverage 0.6400. TVSum: F1 0.6054, Kendall 0.1094, Spearman 0.1549, coverage 1.0000.

Formal command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda PAIR_TAG=unified_strict_phase1_default_formal_seed19500 bash scripts/train_mil_cond_unified_pair.sh`

Formal result:
Log `diagnostics/unified_strict_phase1_default_pair_formal.log`.

SumMe unified formal:
F1 0.4230+/-0.0636, Kendall 0.0295+/-0.0634, Spearman 0.0385+/-0.0867, coverage 0.5840+/-0.0753.

TVSum unified formal:
F1 0.5939+/-0.0244, Kendall 0.1425+/-0.0439, Spearman 0.2061+/-0.0653, coverage 1.0000+/-0.0000.

Decision:
Do not promote the strict paired launcher. The user clarified that unified protocol does not require a single training script or forced shared defaults. Treat this run as an audit, not as the required baseline.

Failure analysis:
Strict unification preserves SumMe but reduces TVSum relative to its dataset-specific best. This confirms the user's concern: the earlier two-dataset pipeline mismatch created a paper-risky comparison. The underlying SumMe bottleneck remains human-preference saliency transfer, not dependency setup, prompt wording alone, or checkpoint selector alone.

Rollback:
Completed after protocol correction: restored the separate SumMe and TVSum launchers and removed `scripts/mil_cond_unified_defaults.sh` plus `scripts/train_mil_cond_unified_pair.sh`.

## 2026-05-10 strict shared-default rollback notes

Hypothesis:
The correct paper protocol is method-level alignment, not one script. Dataset adapters are allowed for paths, splits, logs, and benchmark aggregation; SumMe/TVSum launchers can remain separate if they call the same training/evaluation path and preserve the same input/summary-generation contracts.

Files changed:
Restored `scripts/train_mil_cond_summe_tagr.sh` and `scripts/train_mil_cond_tvsum_tagr.sh`; removed `scripts/mil_cond_unified_defaults.sh` and `scripts/train_mil_cond_unified_pair.sh`. `src/helpers/vsumm_helper.py`, `splits/*.yml`, and Python training/evaluation files were not changed.

Why this does not use frame-level human labels for training:
This is a launcher rollback only. Training targets and pseudo labels remain unchanged and do not use `gtscore` or `user_summary`.

Smoke command:
`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=summe_after_strict_unified_rollback_smoke_seed19500 bash scripts/train_mil_cond_summe_tagr.sh`

`PYTHON_BIN=/data01/anaconda/envs/MMIL_env/bin/python DEVICE=cuda MAX_SPLITS=1 MAX_EPOCH=1 RUN_TAG=tvsum_after_strict_unified_rollback_smoke_seed12345 bash scripts/train_mil_cond_tvsum_tagr.sh`

Formal command:
No formal run was needed for this rollback because it restores the previous launcher contract and both smoke tests passed. Formal method claims should still report SumMe and TVSum under their declared dataset adapter defaults.

Rollback command:
The rollback itself is the desired state. To re-run the rejected audit, recover `scripts/mil_cond_unified_defaults.sh` and `scripts/train_mil_cond_unified_pair.sh` from history or prior artifact, but do not treat it as required protocol.

Main result:
SumMe smoke after rollback: F1 0.4098, Kendall 0.0031, Spearman 0.0077, coverage 0.6400. TVSum smoke after rollback: F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000.

Failure analysis:
The strict shared-default scheme solved the wrong problem. It reduced script/config freedom rather than addressing the actual protocol risks: data schema, split policy, summary budget, summary generation, and method loss/data flow alignment.

Next decision:
Keep separate dataset launcher scripts. For future method changes, preserve method-level protocol alignment and report SumMe plus TVSum impact before promotion.
