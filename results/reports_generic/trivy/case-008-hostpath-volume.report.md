# Benchmark Report: Trivy

**Case:** `case-008-hostpath-volume`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

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
| GT-008 | HostPathVolume | Deployment.benchmark.hostpath-demo | Detected | KSV-0023 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-008-hostpath-volume-0002 | KSV-0023 | GT-008 | Deployment.benchmark.hostpath-demo |

## False positives (3)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-008-hostpath-volume-0001 | KSV-0021 | artifact.yaml |
| trivy-case-008-hostpath-volume-0003 | KSV-0118 | artifact.yaml |
| trivy-case-008-hostpath-volume-0004 | KSV-0121 | artifact.yaml |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-008-hostpath-volume.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-008-hostpath-volume.metrics.json`
- Generated: `2026-09-22T12:10:31.401163+00:00`
