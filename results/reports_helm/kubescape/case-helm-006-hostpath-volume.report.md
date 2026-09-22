# Benchmark Report: Kubescape

**Case:** `case-helm-006-hostpath-volume`

Artifact: `helm_chart` · Mode: `strict` · Status: `complete`

Scanner version: `4.0.14`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 22 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 21 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0455 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.087 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-HELM-006 | HostPathVolume | Deployment.default.hostpath-helm-demo | Detected | C-0048 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| kubescape-case-helm-006-hostpath-volume-0008 | C-0048 | GT-HELM-006 | Deployment.default.hostpath-helm-demo |

## False positives (21)

| Finding | Rule | Resource |
| --- | --- | --- |
| kubescape-case-helm-006-hostpath-volume-0001 | C-0004 | Unknown |
| kubescape-case-helm-006-hostpath-volume-0002 | C-0009 | Unknown |
| kubescape-case-helm-006-hostpath-volume-0003 | C-0013 | Unknown |
| kubescape-case-helm-006-hostpath-volume-0004 | C-0017 | Unknown |
| kubescape-case-helm-006-hostpath-volume-0005 | C-0018 | Unknown |

Showing 5 of 21. See the matched JSON for the full list.

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_helm/kubescape/case-helm-006-hostpath-volume.matched.json`
- Full metrics: `results/metrics_helm/kubescape/case-helm-006-hostpath-volume.metrics.json`
- Generated: `2026-09-22T12:10:56.535310+00:00`
