# Benchmark Report: Checkov

**Case:** `case-docker-018-yum-cache-not-cleaned`

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
| GT-DOCKER-018 | YumCacheNotCleaned | Dockerfile | Missed | — |

## False negatives (1)

| Ground truth | Issue | Resource |
| --- | --- | --- |
| GT-DOCKER-018 | YumCacheNotCleaned | Dockerfile |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_dockerfile/checkov/case-docker-018-yum-cache-not-cleaned.matched.json`
- Full metrics: `results/metrics_dockerfile/checkov/case-docker-018-yum-cache-not-cleaned.metrics.json`
- Generated: `2026-10-01T07:31:35.824941+00:00`
