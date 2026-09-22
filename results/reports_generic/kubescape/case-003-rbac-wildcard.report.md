# Benchmark Report: Kubescape

**Case:** `case-003-rbac-wildcard`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 0 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 0 |
| False negatives | 1 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | Undefined |
| Recall | TP / (TP + FN) | 0 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | Undefined |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-003 | RBACWildcard | Role.benchmark.wildcard-role | Missed | — |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-003 | RBACWildcard | Role.benchmark.wildcard-role |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-003-rbac-wildcard.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-003-rbac-wildcard.metrics.json`
- Generated: `2026-09-22T12:10:27.583799+00:00`
