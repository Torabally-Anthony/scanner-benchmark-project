# Benchmark Report: Checkov

**Case:** `case-helm-004-runs-as-root`

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
| GT-HELM-004 | RunAsRoot | Deployment.default.root-helm-demo | Detected | CKV_K8S_23 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-004-runs-as-root-0012 | CKV_K8S_23 | GT-HELM-004 | Deployment.default.root-helm-demo |

## False positives (13)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-004-runs-as-root-0001 | CKV_K8S_31 | Deployment.default.root-helm-demo |
| checkov-case-helm-004-runs-as-root-0002 | CKV_K8S_8 | Deployment.default.root-helm-demo |
| checkov-case-helm-004-runs-as-root-0003 | CKV_K8S_12 | Deployment.default.root-helm-demo |
| checkov-case-helm-004-runs-as-root-0004 | CKV_K8S_15 | Deployment.default.root-helm-demo |
| checkov-case-helm-004-runs-as-root-0005 | CKV_K8S_13 | Deployment.default.root-helm-demo |

Showing 5 of 13. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-004-runs-as-root.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-004-runs-as-root.metrics.json`
- Generated: `2026-09-22T12:10:54.434855+00:00`
