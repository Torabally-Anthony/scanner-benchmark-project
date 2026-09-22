# Benchmark Report: Kubescape

**Case:** `case-007-missing-resource-limits`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 16 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 13 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 2 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0714 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1333 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-007 | MissingResourceLimits | Deployment.benchmark.no-resource-limits-demo | Detected | C-0009, C-0270, C-0271 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-007-missing-resource-limits-0002 | C-0009 | GT-007 | Deployment.benchmark.no-resource-limits-demo |

## False positives (13)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-007-missing-resource-limits-0001 | C-0004 | Unknown |
| kubescape-case-007-missing-resource-limits-0003 | C-0013 | Unknown |
| kubescape-case-007-missing-resource-limits-0004 | C-0018 | Unknown |
| kubescape-case-007-missing-resource-limits-0005 | C-0030 | Unknown |
| kubescape-case-007-missing-resource-limits-0006 | C-0050 | Unknown |

Showing 5 of 13. See the matched JSON for the full list.

## Duplicate matches (2)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| kubescape-case-007-missing-resource-limits-0015 | C-0270 | GT-007 |
| kubescape-case-007-missing-resource-limits-0016 | C-0271 | GT-007 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-007-missing-resource-limits.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-007-missing-resource-limits.metrics.json`
- Generated: `2026-09-22T12:10:30.841414+00:00`
