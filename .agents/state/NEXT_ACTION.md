# MMIL_D Next Action

Current protocol update:

- `VideoSummarization.md` has been read and its protocol constraints are now active for this project.
- Corrected protocol interpretation: unified experiment protocol means unified method-level pipeline, not one forced launcher or one forced shared-default file.
- Required alignment: same backbone/training entry, same main training logic, same input feature type and H5 schema, same split policy, same 15 percent budget, same keyshot summary generation, and same main loss/data flow unless a new method branch changes them for both datasets.
- Allowed dataset adapters: separate SumMe/TVSum scripts, dataset paths, split files, log/result directories, and benchmark aggregation differences such as SumMe max-F1 and TVSum average-F1.
- The over-constrained `scripts/mil_cond_unified_defaults.sh` and `scripts/train_mil_cond_unified_pair.sh` scheme was rolled back locally and remotely.
- Current dataset launchers:
  - `scripts/train_mil_cond_summe_tagr.sh`
  - `scripts/train_mil_cond_tvsum_tagr.sh`
- The strict shared-default audit from `diagnostics/unified_strict_phase1_default_pair_formal.log` is retained for transparency but is not the required baseline:
  - SumMe: F1 0.4230+/-0.0636, Kendall 0.0295+/-0.0634, Spearman 0.0385+/-0.0867.
  - TVSum: F1 0.5939+/-0.0244, Kendall 0.1425+/-0.0439, Spearman 0.2061+/-0.0653.
- Rollback smoke verification:
  - SumMe: `summe_after_strict_unified_rollback_smoke_seed19500`, F1 0.4098, Kendall 0.0031, Spearman 0.0077, coverage 0.6400.
  - TVSum: `tvsum_after_strict_unified_rollback_smoke_seed12345`, F1 0.6102, Kendall 0.0539, Spearman 0.0835, coverage 1.0000.
- Any next method change should preserve protocol alignment and report both datasets before promotion, but it does not need a single combined launcher.

Current verified bottleneck:

SumMe v3 assets and the first LLM preference teacher improve caption/teacher diagnostics but do not improve the three headline metrics after training under the tested pseudo-teacher, loss, formula, checkpoint-selection, or preference-distillation variants:

- Trusted SumMe baseline: F1 0.4230, Kendall 0.0295, Spearman 0.0385.
- SumMe v3 `phase1_default + budgeted_pseudo_summary` formal: F1 0.4063, Kendall -0.0295, Spearman -0.0401.
- SumMe v3 `phase1_default + hybrid_sparse_budget` formal: F1 0.3973, Kendall -0.0134, Spearman -0.0186.
- SumMe v3 `f1_rank` validation checkpoint selection formal: F1 0.3923, Kendall -0.0302, Spearman -0.0404.
- SumMe `llm_preference_teacher_v1` validation teacher diagnostic: F1 0.5489, Kendall 0.1722, Spearman 0.2200; this beat baseline teacher diagnostics.
- SumMe `preference_distill + llm_preference_teacher_v1` formal: F1 0.3969, Kendall 0.0010, Spearman 0.0010.
- Corrected diagnostic seed mismatch: the original teacher diagnostic used seed 12345, while formal SumMe used seed 19500. Re-running the teacher diagnostic with seed 19500 gives F1 0.4348, Kendall 0.0327, Spearman 0.0458, worse than the seed-matched baseline teacher 0.4389 / 0.0807 / 0.1134.
- A validation-only LLM/baseline score blend grid was also run on seed 19500. Best rank blend at LLM weight 0.15 improved all three metrics over baseline but reached only F1 0.4403, Kendall 0.0886, Spearman 0.1249, so it still fails the absolute F1 gate. No blend row is train-ready.
- `caption_mgs_rank_safe` and `rep_x_anti_redundancy` smokes did not improve the SumMe rank metrics.
- SumMe `adaptive_preference_teacher_v2 + preference_distill` teacher gate passed at F1 0.4726, Kendall 0.1219, Spearman 0.1670, but formal training failed at F1 0.3732, Kendall -0.0411, Spearman -0.0557.
- SumMe `adaptive_preference_teacher_v2 + preference_distill + teacher_rank checkpoint selection` formal also failed at F1 0.3676, Kendall -0.0498, Spearman -0.0672. The selector was hard-rolled back, and default SumMe/TVSum smokes passed afterward.

Next controlled action:

1. Do not promote the tested SumMe v3 formula/loss/checkpoint-selection branches.
2. Do not promote `preference_distill + llm_preference_teacher_v1`; keep rollback active by leaving `RANK_LOSS` and `PREFERENCE_TEACHER_PATH` unset for mainline runs.
3. Do not run additional training with `llm_preference_teacher_v1`; it fails the corrected seed-19500 validation teacher gate.
4. Do not promote `adaptive_preference_teacher_v2 + preference_distill`. Although the adaptive teacher passes seed-19500 validation diagnostics, formal training fails with F1 0.3732, Kendall -0.0411, Spearman -0.0557.
5. Do not promote `teacher_rank` checkpoint selection. It failed formal and has been removed from the code path.
6. Keep `src/build_adaptive_preference_teacher.py` only as a diagnostic/ablation builder unless a new training-transfer branch passes smoke and formal gates.
7. The next safe action is a read-only training-transfer diagnostic, not another score-only teacher or selector:
   - measure per-video gradients/loss contributions from pair/list/inclusion/budget terms on hard SumMe folds;
   - compare teacher shot rank, predicted shot rank, selected keyshots, and validation human rank only for diagnostics;
   - identify whether inclusion BCE, budget regularization, text conditioning, or aggregation from sampled frames to shots is destroying rank.
8. Only after that diagnostic should a new CLI-gated training change be added. Candidate directions are rank-preserving regularization, reliability-weighted loss terms, or a model-side temporal preference head, but none should be run before the transfer failure is localized.
9. Training targets must remain free of `gtscore` / `user_summary`; validation human metrics may be used only for diagnostics/selection, not pseudo-label construction.
10. Run TVSum smoke afterward to confirm default behavior remains unchanged.
11. Update `CURRENT_STATE.md` and append to `EXPERIMENT_LEDGER.md`.
