# Benchmark Report: Kubescape

**Case:** `case-001-privileged-container`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `v4.0.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 23 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 22 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0435 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.0833 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-001 | PrivilegedContainer | Deployment.default.privileged-demo-app | Detected | C-0057 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-001-privileged-container-0012 | C-0057 | GT-001 | Deployment.default.privileged-demo-app |

## False positives (22)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-001-privileged-container-0001 | C-0004 | Unknown |
| kubescape-case-001-privileged-container-0002 | C-0009 | Unknown |
| kubescape-case-001-privileged-container-0003 | C-0013 | Unknown |
| kubescape-case-001-privileged-container-0004 | C-0016 | Unknown |
| kubescape-case-001-privileged-container-0005 | C-0017 | Unknown |

Showing 5 of 22. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/kubescape/case-001-privileged-container.matched.json`
- Full metrics: `results/metrics_generic/kubescape/case-001-privileged-container.metrics.json`
- Generated: `2026-09-17T06:59:44.066914+00:00`
