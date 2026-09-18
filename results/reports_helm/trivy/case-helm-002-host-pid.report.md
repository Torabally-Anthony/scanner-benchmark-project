# Benchmark Report: Trivy

**Case:** `case-helm-002-host-pid`

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
| GT-HELM-002 | HostPID | Deployment.scanner-benchmark.helm-host-pid-demo-app | Detected | KSV-0010 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-helm-002-host-pid-0001 | KSV-0010 | GT-HELM-002 | Deployment.scanner-benchmark.helm-host-pid-demo-app |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/trivy/case-helm-002-host-pid.matched.json`
- Full metrics: `results/metrics_helm/trivy/case-helm-002-host-pid.metrics.json`
- Generated: `2026-09-17T06:59:44.802182+00:00`
