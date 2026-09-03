# Benchmark Report: Kubescape

**Case:** `case-001-privileged-container`

## Benchmark information

| Property | Value |
| --- | --- |
| Case ID | case-001-privileged-container |
| Scanner | Kubescape |
| Artifact type | kubernetes_yaml |
| Matching mode | strict |
| Evaluation status | complete |
| Report generated | 2026-08-02T19:37:38.009343+00:00 |

### Scanner version

```text
Your current version is: v4.0.10
Build commit: f956507357091c3806777fe13ddf5e65efe36e44
Build date: 2026-06-30T05:17:15Z
```

## Results summary

| Measure | Count |
| --- | --- |
| Normalised findings | 23 |
| Ground-truth issues | 1 |
| True positives | 1 |
| False positives | 22 |
| False negatives | 0 |
| Unlabelled extras | 0 |
| Duplicate matches | 0 |
| Ambiguous matches | 0 |

## Performance metrics

| Metric | Formula | Result |
| --- | --- | --- |
| Precision | TP / (TP + FP) | 0.0435 |
| Recall | TP / (TP + FN) | 1 |
| F1 score | 2 * (Precision * Recall) / (Precision + Recall) | 0.0833 |

## Ground-truth evaluation

This table shows whether each known benchmark issue was detected by the scanner.

| Ground truth | Category | Subcategory | Severity | Resource | Container | Field path | Result | Scanner rule |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GT-001 | PodSecurity | PrivilegedContainer | High | Deployment.default.privileged-demo-app | demo-container | spec.template.spec.containers[0].securityContext.privileged | Detected | C-0057 |

## True positives

These findings correctly matched a known ground-truth issue.

| Finding | Rule | Rule name | Ground truth | Severity | Resource | Container | Field path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| kubescape-case-001-privileged-container-0012 | C-0057 | Privileged container | GT-001 | High | Deployment.default.privileged-demo-app | demo-container | spec.template.spec.containers[0].securityContext.privileged |

## False positives

These findings were classified as incorrect according to the selected matching policy.

| Finding | Rule | Rule name | Severity | Resource | Reason |
| --- | --- | --- | --- | --- | --- |
| kubescape-case-001-privileged-container-0001 | C-0004 | Resources memory limit and request | High | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0002 | C-0009 | Resource limits | High | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0003 | C-0013 | Non-root containers | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0004 | C-0016 | Allow privilege escalation | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0005 | C-0017 | Immutable container filesystem | Low | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0006 | C-0018 | Configured readiness probe | Low | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0007 | C-0030 | Ingress and Egress blocked | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0008 | C-0034 | Automatic mapping of service account | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0009 | C-0050 | Resources CPU limit and request | High | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0010 | C-0055 | Linux hardening | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0011 | C-0056 | Configured liveness probe | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0013 | C-0061 | Pods in default namespace | Low | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0014 | C-0077 | K8s common labels usage | Low | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0015 | C-0190 | Ensure that Service Account Tokens are only mounted where necessary | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0016 | C-0210 | Ensure that the seccomp profile is set to docker/default in your pod definitions | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0017 | C-0211 | Apply Security Context to Your Pods and Containers | High | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0018 | C-0237 | Check if signature exists | High | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0019 | C-0260 | Missing network policy | Medium | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0020 | C-0268 | Ensure CPU requests are set | Low | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0021 | C-0269 | Ensure memory requests are set | Low | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0022 | C-0270 | Ensure CPU limits are set | High | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |
| kubescape-case-001-privileged-container-0023 | C-0271 | Ensure memory limits are set | High | Unknown | The finding has no ground-truth mapping and strict mode treats all unmapped findings as false positives. |

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
| Matched findings | results\matched_generic\kubescape\case-001-privileged-container.matched.json | 2026-08-02T19:37:37.479930+00:00 |
| Metrics | results\metrics_generic\kubescape\case-001-privileged-container.metrics.json | 2026-08-02T19:37:37.747202+00:00 |

---

Report generated by the generic scanner benchmark reporting pipeline.
