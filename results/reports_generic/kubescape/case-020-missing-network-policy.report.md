# Benchmark Report: Kubescape

**Case:** `case-020-missing-network-policy`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

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
| GT-020 | MissingNetworkPolicy | Pod.benchmark.missing-network-policy-demo | Detected | C-0030, C-0260 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-020-missing-network-policy-0001 | C-0030 | GT-020 | Pod.benchmark.missing-network-policy-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-020-missing-network-policy-0002 | C-0073 | Unknown |
| kubescape-case-020-missing-network-policy-0003 | C-0077 | Unknown |
| kubescape-case-020-missing-network-policy-0004 | C-0211 | Unknown |
| kubescape-case-020-missing-network-policy-0005 | C-0237 | Unknown |

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| kubescape-case-020-missing-network-policy-0006 | C-0260 | GT-020 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-020-missing-network-policy.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-020-missing-network-policy.metrics.json`
- Generated: `2026-09-26T15:47:09.962955+00:00`
