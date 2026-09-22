# Benchmark Report: Kubescape

**Case:** `case-009-automount-service-account-token`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 11 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 9 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 1 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.1 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1818 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-009 | ServiceAccountToken | Deployment.benchmark.service-account-token-demo | Detected | C-0034, C-0190 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-009-automount-service-account-token-0004 | C-0034 | GT-009 | Deployment.benchmark.service-account-token-demo |

## False positives (9)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-009-automount-service-account-token-0001 | C-0013 | Unknown |
| kubescape-case-009-automount-service-account-token-0002 | C-0018 | Unknown |
| kubescape-case-009-automount-service-account-token-0003 | C-0030 | Unknown |
| kubescape-case-009-automount-service-account-token-0005 | C-0056 | Unknown |
| kubescape-case-009-automount-service-account-token-0006 | C-0076 | Unknown |

Showing 5 of 9. See the matched JSON for the full list.

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| kubescape-case-009-automount-service-account-token-0008 | C-0190 | GT-009 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-009-automount-service-account-token.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-009-automount-service-account-token.metrics.json`
- Generated: `2026-09-22T12:10:32.481856+00:00`
