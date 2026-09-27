# Benchmark Report: Trivy

**Case:** `case-014-privilege-escalation`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

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
| GT-014 | PrivilegeEscalation | Pod.benchmark.privilege-escalation-demo | Detected | KSV-0001 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-014-privilege-escalation-0001 | KSV-0001 | GT-014 | Pod.benchmark.privilege-escalation-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-014-privilege-escalation.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-014-privilege-escalation.metrics.json`
- Generated: `2026-09-26T15:47:05.129711+00:00`
