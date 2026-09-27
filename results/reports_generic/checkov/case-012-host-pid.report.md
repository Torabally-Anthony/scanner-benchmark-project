# Benchmark Report: Checkov

**Case:** `case-012-host-pid`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 1 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
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
| GT-012 | HostPID | Pod.benchmark.host-pid-demo | Detected | CKV_K8S_17 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-012-host-pid-0001 | CKV_K8S_17 | GT-012 | Pod.benchmark.host-pid-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-012-host-pid-0002 | CKV_K8S_43 | Pod.benchmark.host-pid-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-012-host-pid.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-012-host-pid.metrics.json`
- Generated: `2026-09-26T15:47:03.396879+00:00`
