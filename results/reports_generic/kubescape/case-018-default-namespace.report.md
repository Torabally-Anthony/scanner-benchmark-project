# Benchmark Report: Kubescape

**Case:** `case-018-default-namespace`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 5 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 4 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
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
| GT-018 | DefaultNamespace | Pod.default.default-namespace-demo | Detected | C-0061 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-018-default-namespace-0001 | C-0061 | GT-018 | Pod.default.default-namespace-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-018-default-namespace-0002 | C-0073 | Unknown |
| kubescape-case-018-default-namespace-0003 | C-0077 | Unknown |
| kubescape-case-018-default-namespace-0004 | C-0211 | Unknown |
| kubescape-case-018-default-namespace-0005 | C-0237 | Unknown |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-018-default-namespace.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-018-default-namespace.metrics.json`
- Generated: `2026-09-26T15:47:08.451046+00:00`
