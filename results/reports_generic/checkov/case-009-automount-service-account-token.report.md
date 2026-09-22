# Benchmark Report: Checkov

**Case:** `case-009-automount-service-account-token`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 6 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 5 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.1667 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.2857 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-009 | ServiceAccountToken | Deployment.benchmark.service-account-token-demo | Detected | CKV_K8S_38 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-009-automount-service-account-token-0005 | CKV_K8S_38 | GT-009 | Deployment.benchmark.service-account-token-demo |

## False positives (5)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-009-automount-service-account-token-0001 | CKV_K8S_8 | Deployment.benchmark.service-account-token-demo |
| checkov-case-009-automount-service-account-token-0002 | CKV_K8S_15 | Deployment.benchmark.service-account-token-demo |
| checkov-case-009-automount-service-account-token-0003 | CKV_K8S_9 | Deployment.benchmark.service-account-token-demo |
| checkov-case-009-automount-service-account-token-0004 | CKV_K8S_29 | Deployment.benchmark.service-account-token-demo |
| checkov-case-009-automount-service-account-token-0006 | CKV_K8S_43 | Deployment.benchmark.service-account-token-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-009-automount-service-account-token.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-009-automount-service-account-token.metrics.json`
- Generated: `2026-09-22T12:10:31.895936+00:00`
