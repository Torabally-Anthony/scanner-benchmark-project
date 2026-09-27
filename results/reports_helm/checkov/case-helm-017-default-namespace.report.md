# Benchmark Report: Checkov

**Case:** `case-helm-017-default-namespace`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 1 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.5 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.6667 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-017 | DefaultNamespace | Deployment.default.default-namespace-helm-demo | Detected | CKV_K8S_21 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-017-default-namespace-0001 | CKV_K8S_21 | GT-HELM-017 | Deployment.default.default-namespace-helm-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-017-default-namespace-0002 | CKV_K8S_43 | Deployment.default.default-namespace-helm-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-017-default-namespace.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-017-default-namespace.metrics.json`
- Generated: `2026-09-26T16:07:32.421929+00:00`
