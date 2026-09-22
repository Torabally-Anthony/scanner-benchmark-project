# Benchmark Report: Checkov

**Case:** `case-003-rbac-wildcard`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 3 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 2 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.3333 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.5 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-003 | RBACWildcard | Role.benchmark.wildcard-role | Detected | CKV_K8S_49 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-003-rbac-wildcard-0003 | CKV_K8S_49 | GT-003 | Role.benchmark.wildcard-role |

## False positives (2)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-003-rbac-wildcard-0001 | CKV_K8S_158 | Role.benchmark.wildcard-role |
| checkov-case-003-rbac-wildcard-0002 | CKV_K8S_157 | Role.benchmark.wildcard-role |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-003-rbac-wildcard.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-003-rbac-wildcard.metrics.json`
- Generated: `2026-09-22T12:10:27.057158+00:00`
