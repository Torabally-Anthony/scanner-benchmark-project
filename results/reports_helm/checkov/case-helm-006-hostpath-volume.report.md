# Benchmark Report: Checkov

**Case:** `case-helm-006-hostpath-volume`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 12 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 12 |
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
| GT-HELM-006 | HostPathVolume | Deployment.default.hostpath-helm-demo | Missed | — |

## False positives (12)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-006-hostpath-volume-0001 | CKV_K8S_31 | Deployment.default.hostpath-helm-demo |
| checkov-case-helm-006-hostpath-volume-0002 | CKV_K8S_8 | Deployment.default.hostpath-helm-demo |
| checkov-case-helm-006-hostpath-volume-0003 | CKV_K8S_12 | Deployment.default.hostpath-helm-demo |
| checkov-case-helm-006-hostpath-volume-0004 | CKV_K8S_15 | Deployment.default.hostpath-helm-demo |
| checkov-case-helm-006-hostpath-volume-0005 | CKV_K8S_13 | Deployment.default.hostpath-helm-demo |

Showing 5 of 12. See the matched JSON for the full list.

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-HELM-006 | HostPathVolume | Deployment.default.hostpath-helm-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-006-hostpath-volume.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-006-hostpath-volume.metrics.json`
- Generated: `2026-09-22T12:10:55.961339+00:00`
