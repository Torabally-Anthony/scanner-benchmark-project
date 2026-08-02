# Benchmark Report: Checkov

**Case:** `case-001-privileged-container`

## Benchmark information

| Property | Value |
| --- | --- |
| Case ID | case-001-privileged-container |
| Scanner | Checkov |
| Artifact type | kubernetes_yaml |
| Matching mode | review |
| Evaluation status | requires_manual_review |
| Report generated | 2026-08-02T07:32:41.425857+00:00 |

### Scanner version

```text
2.5.20
```

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 20 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extras | 19 |
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
| GT-001 | PodSecurity | PrivilegedContainer | High | Deployment.default.privileged-demo-app | demo-container | spec.template.spec.containers[0].securityContext.privileged | Detected | CKV_K8S_16 |

## True positives

These findings correctly matched a known ground-truth issue.

| Finding | Rule | Rule name | Ground truth | Severity | Resource | Container | Field path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| checkov-case-001-privileged-container-0013 | CKV_K8S_16 | Container should not be privileged | GT-001 | High | Deployment.default.privileged-demo-app | demo-container | spec.template.spec.containers[0].securityContext.privileged |

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
| checkov-case-001-privileged-container-0001 | CKV_K8S_20 | Containers should not run with allowPrivilegeEscalation | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0002 | CKV_K8S_11 | CPU limits should be set | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0003 | CKV_K8S_10 | CPU requests should be set | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0004 | CKV_K8S_21 | The default namespace should not be used | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0005 | CKV_K8S_28 | Minimize the admission of containers with the NET_RAW capability | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0006 | CKV_K8S_43 | Image should use digest | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0007 | CKV_K8S_15 | Image Pull Policy should be Always | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0008 | CKV_K8S_8 | Liveness Probe Should be Configured | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0009 | CKV_K8S_13 | Memory limits should be set | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0010 | CKV_K8S_12 | Memory requests should be set | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0011 | CKV_K8S_37 | Minimize the admission of containers with capabilities assigned | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0012 | CKV_K8S_29 | Apply security context to your pods and containers | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0014 | CKV_K8S_9 | Readiness Probe Should be Configured | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0015 | CKV_K8S_22 | Use read-only filesystem for containers where possible | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0016 | CKV_K8S_23 | Minimize the admission of root containers | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0017 | CKV_K8S_40 | Containers should run as a high UID to avoid host conflict | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0018 | CKV_K8S_31 | Ensure that the seccomp profile is set to docker/default or runtime/default | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0019 | CKV_K8S_38 | Ensure that Service Account Tokens are only mounted where necessary | — | — | — | Deployment.default.privileged-demo-app |
| checkov-case-001-privileged-container-0020 | CKV2_K8S_6 | Minimize the admission of pods which lack an associated NetworkPolicy | — | — | — | Pod.default.privileged-demo-app.app-privileged-demo-app |

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
- **Current limitation:** The scanner reported 19 unlabelled extra finding(s). Therefore, the reported precision only reflects the currently labelled portion of the benchmark results.

## Input provenance

| Input | Path | Generated at |
| --- | --- | --- |
| Matched findings | results\matched_generic\checkov\case-001-privileged-container.matched.json | 2026-08-02T07:32:41.032736+00:00 |
| Metrics | results\metrics_generic\checkov\case-001-privileged-container.metrics.json | 2026-08-02T07:32:41.224863+00:00 |

---

Report generated by the generic scanner benchmark reporting pipeline.
