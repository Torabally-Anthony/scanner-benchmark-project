# Benchmark Report: Trivy

**Case:** `case-010-dangerous-capability`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `Version: 0.74.0`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 5 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 4 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.2 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.3333 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-010 | DangerousCapability | Deployment.benchmark.dangerous-capability-demo | Detected | KSV-0005 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-010-dangerous-capability-0001 | KSV-0005 | GT-010 | Deployment.benchmark.dangerous-capability-demo |

## False positives (4)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-010-dangerous-capability-0002 | KSV-0021 | artifact.yaml |
| trivy-case-010-dangerous-capability-0003 | KSV-0022 | artifact.yaml |
| trivy-case-010-dangerous-capability-0004 | KSV-0106 | artifact.yaml |
| trivy-case-010-dangerous-capability-0005 | KSV-0118 | artifact.yaml |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-010-dangerous-capability.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-010-dangerous-capability.metrics.json`
- Generated: `2026-09-22T12:10:32.974950+00:00`
