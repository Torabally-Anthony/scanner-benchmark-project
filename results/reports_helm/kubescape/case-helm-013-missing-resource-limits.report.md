# Benchmark Report: Kubescape

**Case:** `case-helm-013-missing-resource-limits`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 8 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 3 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 4 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.25 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.4 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-013 | MissingResourceLimits | Deployment.benchmark.missing-resource-limits-helm-demo | Detected | C-0004, C-0009, C-0050, C-0270, C-0271 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-013-missing-resource-limits-0001 | C-0004 | GT-HELM-013 | Deployment.benchmark.missing-resource-limits-helm-demo |

## False positives (3)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-013-missing-resource-limits-0004 | C-0077 | Unknown |
| kubescape-case-helm-013-missing-resource-limits-0005 | C-0211 | Unknown |
| kubescape-case-helm-013-missing-resource-limits-0006 | C-0237 | Unknown |

## Duplicate matches (4)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| kubescape-case-helm-013-missing-resource-limits-0002 | C-0009 | GT-HELM-013 |
| kubescape-case-helm-013-missing-resource-limits-0003 | C-0050 | GT-HELM-013 |
| kubescape-case-helm-013-missing-resource-limits-0007 | C-0270 | GT-HELM-013 |
| kubescape-case-helm-013-missing-resource-limits-0008 | C-0271 | GT-HELM-013 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-013-missing-resource-limits.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-013-missing-resource-limits.metrics.json`
- Generated: `2026-10-02T10:34:52.993833+00:00`
