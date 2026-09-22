# Benchmark Report: Checkov

**Case:** `case-docker-004-exposed-ssh-port`

Artifact: `dockerfile` · Mode: `strict` · Status: `complete`

Scanner version: `3.3.10`

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
| GT-DOCKER-004 | SSHExposure | Dockerfile | Detected | CKV_DOCKER_1 |

## True positives (1)

| Finding | Rule | Ground truth | Resource |
| --- | --- | --- | --- |
| checkov-case-docker-004-exposed-ssh-port-0001 | CKV_DOCKER_1 | GT-DOCKER-004 | Dockerfile |

Unmapped findings count as false positives; duplicate and ambiguous matches are excluded from the scores.

- Full findings: `results/matched_dockerfile/checkov/case-docker-004-exposed-ssh-port.matched.json`
- Full metrics: `results/metrics_dockerfile/checkov/case-docker-004-exposed-ssh-port.metrics.json`
- Generated: `2026-09-22T12:10:34.693104+00:00`
