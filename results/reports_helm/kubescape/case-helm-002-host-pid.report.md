# Benchmark Report: Kubescape

**Case:** `case-helm-002-host-pid`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `v4.0.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 7 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 6 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.1429 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.25 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-002 | HostPID | Deployment.scanner-benchmark.helm-host-pid-demo-app | Detected | C-0038 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-002-host-pid-0002 | C-0038 | GT-HELM-002 | Deployment.scanner-benchmark.helm-host-pid-demo-app |

## False positives (6)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-002-host-pid-0001 | C-0030 | Unknown |
| kubescape-case-helm-002-host-pid-0003 | C-0077 | Unknown |
| kubescape-case-helm-002-host-pid-0004 | C-0211 | Unknown |
| kubescape-case-helm-002-host-pid-0005 | C-0237 | Unknown |
| kubescape-case-helm-002-host-pid-0006 | C-0260 | Unknown |

Showing 5 of 6. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-002-host-pid.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-002-host-pid.metrics.json`
- Generated: `2026-09-17T06:59:44.691737+00:00`
