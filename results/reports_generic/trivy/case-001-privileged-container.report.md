# Benchmark Report: Trivy

**Case:** `case-001-privileged-container`

## Benchmark information

| Property | Value |
| --- | --- |
| Case ID | case-001-privileged-container |
| Scanner | Trivy |
| Artifact type | kubernetes_yaml |
| Matching mode | strict |
| Evaluation status | complete |
| Report generated | 2026-08-02T19:37:36.590545+00:00 |

### Scanner version

```text
Unknown
```

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 18 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 17 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0556 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.1053 |

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

| Finding | Rule | Rule name | Severity | Resource | Reason |
| --- | --- | --- | --- | --- | --- |
| trivy-case-001-privileged-container-0001 | KSV-0001 | Can elevate its own privileges | MEDIUM | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0002 | KSV-0003 | Default capabilities: some containers do not drop all | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0003 | KSV-0004 | Default capabilities: some containers do not drop any | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0004 | KSV-0011 | CPU not limited | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0005 | KSV-0012 | Runs as root user | MEDIUM | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0006 | KSV-0014 | Root file system is not read-only | HIGH | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0007 | KSV-0015 | CPU requests not specified | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0008 | KSV-0016 | Memory requests not specified | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0010 | KSV-0018 | Memory not limited | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0011 | KSV-0020 | Runs with UID <= 10000 | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0012 | KSV-0021 | Runs with GID <= 10000 | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0013 | KSV-0030 | Runtime/Default Seccomp profile not set | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0014 | KSV-0104 | Seccomp policies disabled | MEDIUM | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0015 | KSV-0106 | Container capabilities must only include NET_BIND_SERVICE | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0016 | KSV-0110 | Workloads in the default namespace | LOW | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0017 | KSV-0117 | Prevent binding to privileged ports | MEDIUM | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| trivy-case-001-privileged-container-0018 | KSV-0118 | Default security context configured | HIGH | artifact.yaml | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |

## False negatives

These ground-truth issues were not detected by the scanner.

No findings were recorded in this category.

## Unlabelled extra findings

These scanner findings do not yet have an approved mapping to the benchmark ground truth.

No findings were recorded in this category.

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
- **Strict-mode policy:** Unmapped findings are counted as false positives.
- **Duplicate policy:** Only the first valid finding mapped to a ground-truth issue is counted as a true positive. Additional detections of the same issue are stored as duplicate matches.
- **Ambiguous findings:** Ambiguous matches are reported separately and are excluded from the precision, recall and F1 calculations.

## Input provenance

| Input | Path | Generated at |
| --- | --- | --- |
| Matched findings | results\matched_generic\trivy\case-001-privileged-container.matched.json | 2026-08-02T19:37:35.808312+00:00 |
| Metrics | results\metrics_generic\trivy\case-001-privileged-container.metrics.json | 2026-08-02T19:37:36.147332+00:00 |

---

Report generated by the generic scanner benchmark reporting pipeline.
