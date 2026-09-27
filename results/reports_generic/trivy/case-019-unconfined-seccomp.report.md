# Benchmark Report: Trivy

**Case:** `case-019-unconfined-seccomp`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 1 |
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
| GT-019 | UnconfinedSeccomp | Pod.benchmark.unconfined-seccomp-demo | Detected | KSV-0030, KSV-0104 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-019-unconfined-seccomp-0001 | KSV-0030 | GT-019 | Pod.benchmark.unconfined-seccomp-demo |

## Duplicate matches (1)

| Finding | Rule | Ground truth |
| --- | --- | --- |
| trivy-case-019-unconfined-seccomp-0002 | KSV-0104 | GT-019 |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-019-unconfined-seccomp.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-019-unconfined-seccomp.metrics.json`
- Generated: `2026-09-26T15:47:08.922409+00:00`
