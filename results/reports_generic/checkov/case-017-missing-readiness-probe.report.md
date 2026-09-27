# Benchmark Report: Checkov

**Case:** `case-017-missing-readiness-probe`

Artifact: `kubernetes_yaml` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 2 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 1 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.5 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.6667 |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-017 | MissingReadinessProbe | Pod.benchmark.missing-readiness-probe-demo | Detected | CKV_K8S_9 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-017-missing-readiness-probe-0001 | CKV_K8S_9 | GT-017 | Pod.benchmark.missing-readiness-probe-demo |

## False positives (1)

| Finding | Rule | Resource |
| --- | --- | --- |
| checkov-case-017-missing-readiness-probe-0002 | CKV_K8S_43 | Pod.benchmark.missing-readiness-probe-demo |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_generic/checkov/case-017-missing-readiness-probe.matched.json`
- Full metrics: `results/metrics_generic/checkov/case-017-missing-readiness-probe.metrics.json`
- Generated: `2026-09-26T15:47:07.161149+00:00`
