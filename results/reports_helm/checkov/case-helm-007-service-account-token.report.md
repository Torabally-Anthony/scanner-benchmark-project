# Benchmark Report: Checkov

**Case:** `case-helm-007-service-account-token`

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
| GT-HELM-007 | ServiceAccountToken | Deployment.default.token-helm-demo | Detected | CKV_K8S_38 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-007-service-account-token-0010 | CKV_K8S_38 | GT-HELM-007 | Deployment.default.token-helm-demo |

## False positives (12)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-007-service-account-token-0001 | CKV_K8S_31 | Deployment.default.token-helm-demo |
| checkov-case-helm-007-service-account-token-0002 | CKV_K8S_8 | Deployment.default.token-helm-demo |
| checkov-case-helm-007-service-account-token-0003 | CKV_K8S_12 | Deployment.default.token-helm-demo |
| checkov-case-helm-007-service-account-token-0004 | CKV_K8S_15 | Deployment.default.token-helm-demo |
| checkov-case-helm-007-service-account-token-0005 | CKV_K8S_13 | Deployment.default.token-helm-demo |

Showing 5 of 12. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-007-service-account-token.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-007-service-account-token.metrics.json`
- Generated: `2026-09-22T12:10:56.781462+00:00`
