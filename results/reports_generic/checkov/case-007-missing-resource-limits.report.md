# Benchmark Report: Checkov

**Case:** `case-007-missing-resource-limits`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 9 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 7 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 1 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.125 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.2222 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-007 | MissingResourceLimits | Deployment.benchmark.no-resource-limits-demo | Detected | CKV_K8S_11, CKV_K8S_13 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-007-missing-resource-limits-0004 | CKV_K8S_13 | GT-007 | Deployment.benchmark.no-resource-limits-demo |

## False positives (7)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-007-missing-resource-limits-0001 | CKV_K8S_8 | Deployment.benchmark.no-resource-limits-demo |
| checkov-case-007-missing-resource-limits-0002 | CKV_K8S_12 | Deployment.benchmark.no-resource-limits-demo |
| checkov-case-007-missing-resource-limits-0003 | CKV_K8S_15 | Deployment.benchmark.no-resource-limits-demo |
| checkov-case-007-missing-resource-limits-0005 | CKV_K8S_10 | Deployment.benchmark.no-resource-limits-demo |
| checkov-case-007-missing-resource-limits-0006 | CKV_K8S_9 | Deployment.benchmark.no-resource-limits-demo |

Showing 5 of 7. See the matched JSON for the full list.

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| checkov-case-007-missing-resource-limits-0009 | CKV_K8S_11 | GT-007 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-007-missing-resource-limits.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-007-missing-resource-limits.metrics.json`
- Generated: `2026-09-22T12:10:30.355038+00:00`
