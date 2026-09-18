# Benchmark Report: Checkov

**Case:** `case-helm-002-host-pid`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `2.5.20`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 4 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 3 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.25 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.4 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-002 | HostPID | Deployment.scanner-benchmark.helm-host-pid-demo-app | Detected | CKV_K8S_17 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-helm-002-host-pid-0003 | CKV_K8S_17 | GT-HELM-002 | Deployment.scanner-benchmark.helm-host-pid-demo-app |

## False positives (3)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-helm-002-host-pid-0001 | CKV_K8S_43 | Deployment.scanner-benchmark.helm-host-pid-demo-app |
| checkov-case-helm-002-host-pid-0002 | CKV_K8S_15 | Deployment.scanner-benchmark.helm-host-pid-demo-app |
| checkov-case-helm-002-host-pid-0004 | CKV2_K8S_6 | Pod.scanner-benchmark.helm-host-pid-demo-app.app-helm-host-pid-demo-app |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/checkov/case-helm-002-host-pid.matched.json`
- Full metrics: `results/metrics_helm/checkov/case-helm-002-host-pid.metrics.json`
- Generated: `2026-09-17T06:59:44.580347+00:00`
