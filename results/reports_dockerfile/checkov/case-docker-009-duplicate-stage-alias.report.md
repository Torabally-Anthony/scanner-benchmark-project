# Benchmark Report: Checkov

**Case:** `case-docker-009-duplicate-stage-alias`

Artifact: `dockerfile` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 0 |
| Ground-truth issues | 1 |
| True positives | 0 |
| False positives | 0 |
| False negatives | 1 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | Undefined |
| Recall | TP / (TP + FN) | 0 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | Undefined |

## Ground-truth evaluation

| Ground truth | Issue | Resource | Result | Scanner rule |
| --- | --- | --- | --- | --- |
| GT-DOCKER-009 | DuplicateStageAlias | Dockerfile | Missed | — |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-DOCKER-009 | DuplicateStageAlias | Dockerfile |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_dockerfile/checkov/case-docker-009-duplicate-stage-alias.matched.json`
- Full metrics: `results/metrics_dockerfile/checkov/case-docker-009-duplicate-stage-alias.metrics.json`
- Generated: `2026-09-22T12:10:37.256281+00:00`
