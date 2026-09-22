# Benchmark Report: Trivy

**Case:** `case-docker-005-missing-healthcheck`

Artifact: `dockerfile` · Mode: `strict` · Status: `complete`

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
| GT-DOCKER-005 | MissingHealthcheck | Dockerfile | Detected | DS-0026 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| trivy-case-docker-005-missing-healthcheck-0001 | DS-0026 | GT-DOCKER-005 | Dockerfile |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_dockerfile/trivy/case-docker-005-missing-healthcheck.matched.json`
- Full metrics: `results/metrics_dockerfile/trivy/case-docker-005-missing-healthcheck.metrics.json`
- Generated: `2026-09-22T12:10:35.453917+00:00`
