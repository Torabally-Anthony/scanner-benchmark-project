# Benchmark Report: Trivy

**Case:** `case-helm-010-public-loadbalancer`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 0 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 0 |
| False negatives | 1 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | Undefined |
| Recall | TP / (TP + FN) | 0 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | Undefined |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-010 | ExternalExposure | Service.default.public-helm-service | Missed | — |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-HELM-010 | ExternalExposure | Service.default.public-helm-service |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-010-public-loadbalancer.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-010-public-loadbalancer.metrics.json`
- Generated: `2026-09-22T12:10:59.487640+00:00`
