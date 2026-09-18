# Benchmark Report: Trivy

**Case:** `case-helm-001-host-network`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

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
| GT-HELM-001 | HostNetwork | Deployment.scanner-benchmark.helm-host-network-demo-app | Detected | KSV-0009 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-helm-001-host-network-0001 | KSV-0009 | GT-HELM-001 | Deployment.scanner-benchmark.helm-host-network-demo-app |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-001-host-network.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-001-host-network.metrics.json`
- Generated: `2026-09-17T06:59:44.747141+00:00`
