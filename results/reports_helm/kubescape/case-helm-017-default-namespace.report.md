# Benchmark Report: Kubescape

**Case:** `case-helm-017-default-namespace`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 4 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 3 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
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
| GT-HELM-017 | DefaultNamespace | Deployment.default.default-namespace-helm-demo | Detected | C-0061 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-017-default-namespace-0001 | C-0061 | GT-HELM-017 | Deployment.default.default-namespace-helm-demo |

## False positives (3)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-017-default-namespace-0002 | C-0077 | Unknown |
| kubescape-case-helm-017-default-namespace-0003 | C-0211 | Unknown |
| kubescape-case-helm-017-default-namespace-0004 | C-0237 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-017-default-namespace.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-017-default-namespace.metrics.json`
- Generated: `2026-09-26T16:07:32.865042+00:00`
