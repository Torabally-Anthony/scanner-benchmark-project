# Benchmark Report: Kubescape

**Case:** `case-008-hostpath-volume`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 11 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 10 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0909 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1667 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-008 | HostPathVolume | Deployment.benchmark.hostpath-demo | Detected | C-0048 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-008-hostpath-volume-0005 | C-0048 | GT-008 | Deployment.benchmark.hostpath-demo |

## False positives (10)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-008-hostpath-volume-0001 | C-0013 | Unknown |
| kubescape-case-008-hostpath-volume-0002 | C-0018 | Unknown |
| kubescape-case-008-hostpath-volume-0003 | C-0030 | Unknown |
| kubescape-case-008-hostpath-volume-0004 | C-0045 | Unknown |
| kubescape-case-008-hostpath-volume-0006 | C-0056 | Unknown |

Showing 5 of 10. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-008-hostpath-volume.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-008-hostpath-volume.metrics.json`
- Generated: `2026-09-22T12:10:31.643640+00:00`
