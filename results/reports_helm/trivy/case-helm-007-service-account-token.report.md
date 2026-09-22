# Benchmark Report: Trivy

**Case:** `case-helm-007-service-account-token`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 10 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 10 |
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
| GT-HELM-007 | ServiceAccountToken | Deployment.default.token-helm-demo | Missed | — |

## False positives (10)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-helm-007-service-account-token-0001 | KSV-0011 | templates/deployment.yaml |
| trivy-case-helm-007-service-account-token-0002 | KSV-0014 | templates/deployment.yaml |
| trivy-case-helm-007-service-account-token-0003 | KSV-0015 | templates/deployment.yaml |
| trivy-case-helm-007-service-account-token-0004 | KSV-0016 | templates/deployment.yaml |
| trivy-case-helm-007-service-account-token-0005 | KSV-0018 | templates/deployment.yaml |

Showing 5 of 10. See the matched JSON for the full list.

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-HELM-007 | ServiceAccountToken | Deployment.default.token-helm-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-007-service-account-token.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-007-service-account-token.metrics.json`
- Generated: `2026-09-22T12:10:57.027596+00:00`
