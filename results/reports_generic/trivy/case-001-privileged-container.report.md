# Benchmark Report: Trivy

**Case:** `case-001-privileged-container`

## Benchmark information

| Property | Value |
| --- | --- |
| Case ID | case-001-privileged-container |
| Scanner | Trivy |
| Artifact type | kubernetes_yaml |
| Matching mode | review |
| Evaluation status | requires_manual_review |
| Report generated | 2026-08-02T07:32:42.214320+00:00 |

### Scanner version

```text
Version: 0.69.3
Vulnerability DB:
  Version: 2
  UpdatedAt: 2026-04-06 12:43:27.029798302 +0000 UTC
  NextUpdate: 2026-04-07 12:43:27.02979735 +0000 UTC
  DownloadedAt: 2026-04-06 18:21:27.0765915 +0000 UTC
Check Bundle:
  Digest: sha256:1583562f8b90ed2a071b99f0e5ffff6b57e4ceb6ca3e4796577b4e6a339eb74c
  DownloadedAt: 2026-07-23 05:42:39.3164487 +0000 UTC
```

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 18 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extras | 17 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 1 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 1 |

## Ground-truth evaluation

This table shows whether each known benchmark issue was detected by the scanner.

| Ground truth | Category | Subcategory | Severity | Resource | Container | Field path | Result | Scanner rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GT-001 | PodSecurity | PrivilegedContainer | High | Deployment.default.privileged-demo-app | demo-container | spec.template.spec.containers[0].securityContext.privileged | Detected | KSV-0017 |

## True positives

These findings correctly matched a known ground-truth issue.

| Finding | Rule | Rule name | Ground truth | Severity | Resource | Container | Field path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| trivy-case-001-privileged-container-0009 | KSV-0017 | Privileged | GT-001 | High | Deployment.default.privileged-demo-app | demo-container | spec.template.spec.containers[0].securityContext.privileged |

## False positives

These findings were classified as incorrect according to the selected matching policy.

No findings were recorded in this category.

## False negatives

These ground-truth issues were not detected by the scanner.

No findings were recorded in this category.

## Unlabelled extra findings

These scanner findings do not yet have an approved mapping to the benchmark ground truth.

| Finding | Rule | Rule name | Severity | Original category | Original subcategory | Resource |
| --- | --- | --- | --- | --- | --- | --- |
| trivy-case-001-privileged-container-0001 | KSV-0001 | Can elevate its own privileges | MEDIUM | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0002 | KSV-0003 | Default capabilities: some containers do not drop all | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0003 | KSV-0004 | Default capabilities: some containers do not drop any | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0004 | KSV-0011 | CPU not limited | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0005 | KSV-0012 | Runs as root user | MEDIUM | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0006 | KSV-0014 | Root file system is not read-only | HIGH | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0007 | KSV-0015 | CPU requests not specified | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0008 | KSV-0016 | Memory requests not specified | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0010 | KSV-0018 | Memory not limited | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0011 | KSV-0020 | Runs with UID <= 10000 | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0012 | KSV-0021 | Runs with GID <= 10000 | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0013 | KSV-0030 | Runtime/Default Seccomp profile not set | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0014 | KSV-0104 | Seccomp policies disabled | MEDIUM | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0015 | KSV-0106 | Container capabilities must only include NET_BIND_SERVICE | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0016 | KSV-0110 | Workloads in the default namespace | LOW | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0017 | KSV-0117 | Prevent binding to privileged ports | MEDIUM | config | kubernetes | artifact.yaml |
| trivy-case-001-privileged-container-0018 | KSV-0118 | Default security context configured | HIGH | config | kubernetes | artifact.yaml |

## Duplicate matches

These additional findings matched an issue that had already been counted as a true positive.

No findings were recorded in this category.

## Ambiguous matches

These findings contained incomplete or inconsistent mapping information.

No findings were recorded in this category.

## Interpretation and methodological notes

- **Precision:** Precision measures the proportion of classified positive findings that were true positives.
- **Recall:** Recall measures the proportion of ground-truth issues detected by the scanner.
- **F1 score:** F1 is the harmonic mean of precision and recall.
- **Review-mode policy:** Unmapped findings are retained as unlabelled extras. They are not counted as false positives until they have been manually reviewed.
- **Duplicate policy:** Only the first valid finding mapped to a ground-truth issue is counted as a true positive. Additional detections of the same issue are stored as duplicate matches.
- **Ambiguous findings:** Ambiguous matches are reported separately and are excluded from the precision, recall and F1 calculations.
- **Current limitation:** The scanner reported 17 unlabelled extra finding(s). Therefore, the reported precision only reflects the currently labelled portion of the benchmark results.

## Input provenance

| Input | Path | Generated at |
| --- | --- | --- |
| Matched findings | results\matched_generic\trivy\case-001-privileged-container.matched.json | 2026-08-02T07:32:41.815924+00:00 |
| Metrics | results\metrics_generic\trivy\case-001-privileged-container.metrics.json | 2026-08-02T07:32:42.019050+00:00 |

---

Report generated by the generic scanner benchmark reporting pipeline.
