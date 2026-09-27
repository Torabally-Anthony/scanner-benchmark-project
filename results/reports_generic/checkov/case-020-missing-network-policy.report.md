# Benchmark Report: Checkov

**Case:** `case-020-missing-network-policy`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

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
| GT-020 | MissingNetworkPolicy | Pod.benchmark.missing-network-policy-demo | Missed | — |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-020-missing-network-policy-0001 | CKV_K8S_43 | Pod.benchmark.missing-network-policy-demo |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-020 | MissingNetworkPolicy | Pod.benchmark.missing-network-policy-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-020-missing-network-policy.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-020-missing-network-policy.metrics.json`
- Generated: `2026-09-26T15:47:09.540316+00:00`
