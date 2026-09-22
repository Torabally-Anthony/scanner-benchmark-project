# Benchmark Report: Trivy

**Case:** `case-007-missing-resource-limits`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 6 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 4 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 1 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.2 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.3333 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-007 | MissingResourceLimits | Deployment.benchmark.no-resource-limits-demo | Detected | KSV-0011, KSV-0018 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-007-missing-resource-limits-0001 | KSV-0011 | GT-007 | Deployment.benchmark.no-resource-limits-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-007-missing-resource-limits-0002 | KSV-0015 | artifact.yaml |
| trivy-case-007-missing-resource-limits-0003 | KSV-0016 | artifact.yaml |
| trivy-case-007-missing-resource-limits-0005 | KSV-0021 | artifact.yaml |
| trivy-case-007-missing-resource-limits-0006 | KSV-0118 | artifact.yaml |

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| trivy-case-007-missing-resource-limits-0004 | KSV-0018 | GT-007 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-007-missing-resource-limits.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-007-missing-resource-limits.metrics.json`
- Generated: `2026-09-22T12:10:30.597339+00:00`
