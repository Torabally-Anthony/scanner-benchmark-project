# Benchmark Report: Checkov

**Case:** `case-helm-003-privileged-container`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 13 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 12 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0769 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1429 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-003 | PrivilegedContainer | Deployment.default.privileged-helm-demo | Detected | CKV_K8S_16 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-003-privileged-container-0007 | CKV_K8S_16 | GT-HELM-003 | Deployment.default.privileged-helm-demo |

## False positives (12)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-003-privileged-container-0001 | CKV_K8S_31 | Deployment.default.privileged-helm-demo |
| checkov-case-helm-003-privileged-container-0002 | CKV_K8S_8 | Deployment.default.privileged-helm-demo |
| checkov-case-helm-003-privileged-container-0003 | CKV_K8S_12 | Deployment.default.privileged-helm-demo |
| checkov-case-helm-003-privileged-container-0004 | CKV_K8S_15 | Deployment.default.privileged-helm-demo |
| checkov-case-helm-003-privileged-container-0005 | CKV_K8S_13 | Deployment.default.privileged-helm-demo |

Showing 5 of 12. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-003-privileged-container.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-003-privileged-container.metrics.json`
- Generated: `2026-09-22T12:10:38.288753+00:00`
