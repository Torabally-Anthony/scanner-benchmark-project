# Benchmark Report: Kubescape

**Case:** `case-013-host-ipc`

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
| GT-013 | HostIPC | Pod.benchmark.host-ipc-demo | Detected | C-0038, C-0276 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-013-host-ipc-0001 | C-0038 | GT-013 | Pod.benchmark.host-ipc-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-013-host-ipc-0002 | C-0073 | Unknown |
| kubescape-case-013-host-ipc-0003 | C-0077 | Unknown |
| kubescape-case-013-host-ipc-0004 | C-0211 | Unknown |
| kubescape-case-013-host-ipc-0005 | C-0237 | Unknown |

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| kubescape-case-013-host-ipc-0006 | C-0276 | GT-013 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-013-host-ipc.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-013-host-ipc.metrics.json`
- Generated: `2026-09-26T16:18:11.272548+00:00`
