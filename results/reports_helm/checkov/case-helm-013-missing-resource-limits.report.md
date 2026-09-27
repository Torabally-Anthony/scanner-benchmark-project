# Benchmark Report: Checkov

**Case:** `case-helm-013-missing-resource-limits`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 3 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 1 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 1 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.5 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.6667 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-013 | MissingResourceLimits | Deployment.benchmark.missing-resource-limits-helm-demo | Detected | CKV_K8S_11, CKV_K8S_13 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-013-missing-resource-limits-0001 | CKV_K8S_13 | GT-HELM-013 | Deployment.benchmark.missing-resource-limits-helm-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-013-missing-resource-limits-0002 | CKV_K8S_43 | Deployment.benchmark.missing-resource-limits-helm-demo |

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| checkov-case-helm-013-missing-resource-limits-0003 | CKV_K8S_11 | GT-HELM-013 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-013-missing-resource-limits.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-013-missing-resource-limits.metrics.json`
- Generated: `2026-09-26T16:07:29.444749+00:00`
