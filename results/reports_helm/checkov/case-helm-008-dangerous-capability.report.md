# Benchmark Report: Checkov

**Case:** `case-helm-008-dangerous-capability`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 14 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 13 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0714 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1333 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-008 | DangerousCapability | Deployment.default.capability-helm-demo | Detected | CKV_K8S_39 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-008-dangerous-capability-0007 | CKV_K8S_39 | GT-HELM-008 | Deployment.default.capability-helm-demo |

## False positives (13)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-008-dangerous-capability-0001 | CKV_K8S_31 | Deployment.default.capability-helm-demo |
| checkov-case-helm-008-dangerous-capability-0002 | CKV_K8S_8 | Deployment.default.capability-helm-demo |
| checkov-case-helm-008-dangerous-capability-0003 | CKV_K8S_12 | Deployment.default.capability-helm-demo |
| checkov-case-helm-008-dangerous-capability-0004 | CKV_K8S_15 | Deployment.default.capability-helm-demo |
| checkov-case-helm-008-dangerous-capability-0005 | CKV_K8S_13 | Deployment.default.capability-helm-demo |

Showing 5 of 13. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-008-dangerous-capability.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-008-dangerous-capability.metrics.json`
- Generated: `2026-09-22T12:10:57.589784+00:00`
