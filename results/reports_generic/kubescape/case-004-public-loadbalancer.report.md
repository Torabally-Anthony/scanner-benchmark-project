# Benchmark Report: Kubescape

**Case:** `case-004-public-loadbalancer`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 1 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 1 |
| False negatives | 1 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0 |
| Recall | TP / (TP + FN) | 0 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-004 | ExternalExposure | Service.benchmark.public-demo-service | Missed | — |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-004-public-loadbalancer-0001 | C-0293 | Unknown |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-004 | ExternalExposure | Service.benchmark.public-demo-service |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-004-public-loadbalancer.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-004-public-loadbalancer.metrics.json`
- Generated: `2026-09-22T12:10:28.351750+00:00`
