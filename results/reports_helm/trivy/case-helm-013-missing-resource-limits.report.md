# Benchmark Report: Trivy

**Case:** `case-helm-013-missing-resource-limits`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 1 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 1 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 1 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-013 | MissingResourceLimits | Deployment.benchmark.missing-resource-limits-helm-demo | Detected | KSV-0011, KSV-0018 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-helm-013-missing-resource-limits-0001 | KSV-0011 | GT-HELM-013 | Deployment.benchmark.missing-resource-limits-helm-demo |

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| trivy-case-helm-013-missing-resource-limits-0002 | KSV-0018 | GT-HELM-013 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-013-missing-resource-limits.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-013-missing-resource-limits.metrics.json`
- Generated: `2026-09-26T16:07:29.663235+00:00`
