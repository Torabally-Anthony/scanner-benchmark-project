# Benchmark Report: Checkov

**Case:** `case-008-hostpath-volume`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 5 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 5 |
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
| GT-008 | HostPathVolume | Deployment.benchmark.hostpath-demo | Missed | — |

## False positives (5)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-008-hostpath-volume-0001 | CKV_K8S_8 | Deployment.benchmark.hostpath-demo |
| checkov-case-008-hostpath-volume-0002 | CKV_K8S_15 | Deployment.benchmark.hostpath-demo |
| checkov-case-008-hostpath-volume-0003 | CKV_K8S_9 | Deployment.benchmark.hostpath-demo |
| checkov-case-008-hostpath-volume-0004 | CKV_K8S_29 | Deployment.benchmark.hostpath-demo |
| checkov-case-008-hostpath-volume-0005 | CKV_K8S_43 | Deployment.benchmark.hostpath-demo |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-008 | HostPathVolume | Deployment.benchmark.hostpath-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-008-hostpath-volume.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-008-hostpath-volume.metrics.json`
- Generated: `2026-09-22T12:10:31.144321+00:00`
