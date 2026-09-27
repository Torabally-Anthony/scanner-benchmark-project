# Benchmark Report: Trivy

**Case:** `case-helm-017-default-namespace`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 1 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 1 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 1 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-017 | DefaultNamespace | Deployment.default.default-namespace-helm-demo | Detected | KSV-0110 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-helm-017-default-namespace-0001 | KSV-0110 | GT-HELM-017 | Deployment.default.default-namespace-helm-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-017-default-namespace.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-017-default-namespace.metrics.json`
- Generated: `2026-09-26T16:07:32.643396+00:00`
