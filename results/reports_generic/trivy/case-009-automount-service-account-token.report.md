# Benchmark Report: Trivy

**Case:** `case-009-automount-service-account-token`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 2 |
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
| GT-009 | ServiceAccountToken | Deployment.benchmark.service-account-token-demo | Missed | — |

## False positives (2)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-009-automount-service-account-token-0001 | KSV-0021 | artifact.yaml |
| trivy-case-009-automount-service-account-token-0002 | KSV-0118 | artifact.yaml |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-009 | ServiceAccountToken | Deployment.benchmark.service-account-token-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-009-automount-service-account-token.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-009-automount-service-account-token.metrics.json`
- Generated: `2026-09-22T12:10:32.232376+00:00`
