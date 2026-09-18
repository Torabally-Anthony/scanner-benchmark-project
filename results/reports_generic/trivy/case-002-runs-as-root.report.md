# Benchmark Report: Trivy

**Case:** `case-002-runs-as-root`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

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
| GT-002 | RunsAsRoot | Deployment.scanner-benchmark.runs-as-root-demo-app | Detected | KSV-0012 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-002-runs-as-root-0001 | KSV-0012 | GT-002 | Deployment.scanner-benchmark.runs-as-root-demo-app |

## False positives (3)

| Finding | Rule | Resource |
| --- | --- | --- |
| trivy-case-002-runs-as-root-0002 | KSV-0020 | artifact.yaml |
| trivy-case-002-runs-as-root-0003 | KSV-0021 | artifact.yaml |
| trivy-case-002-runs-as-root-0004 | KSV-0117 | artifact.yaml |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/trivy/case-002-runs-as-root.matched.json`
- Full metrics: `results/metrics_generic/trivy/case-002-runs-as-root.metrics.json`
- Generated: `2026-09-17T06:59:44.234898+00:00`
