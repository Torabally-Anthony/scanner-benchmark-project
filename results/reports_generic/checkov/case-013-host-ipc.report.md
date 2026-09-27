# Benchmark Report: Checkov

**Case:** `case-013-host-ipc`

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
| GT-013 | HostIPC | Pod.benchmark.host-ipc-demo | Detected | CKV_K8S_18 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-013-host-ipc-0001 | CKV_K8S_18 | GT-013 | Pod.benchmark.host-ipc-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-013-host-ipc-0002 | CKV_K8S_43 | Pod.benchmark.host-ipc-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-013-host-ipc.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-013-host-ipc.metrics.json`
- Generated: `2026-09-26T16:18:10.725246+00:00`
