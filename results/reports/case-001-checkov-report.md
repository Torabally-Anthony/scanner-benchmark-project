# Case 001 Checkov Benchmark Report

## 1. Case Summary

**Case ID:** `case-001-privileged-container`  
**Tool:** `checkov`  
**Artifact type:** `kubernetes_yaml`  
**Matching mode:** `review_mode`  

This benchmark case tests whether Checkov can detect a Kubernetes container running in privileged mode.

The intentional ground-truth misconfiguration is:

`securityContext.privileged: true`

## 2. Ground-Truth Detection Result

Checkov successfully detected the intended privileged-container misconfiguration.

## 3. True Positive Finding

- **Ground-truth ID:** `GT-001`
- **Scanner rule ID:** `CKV_K8S_16`
- **Scanner rule name:** Container should not be privileged
- **Category:** `PodSecurity`
- **Subcategory:** `PrivilegedContainer`
- **Resource:** `Deployment.default.privileged-demo-app`
- **Field path:** `spec.template.spec.containers[0].securityContext.privileged`
- **Match status:** `true_positive`

## 4. Metric Counts

| Count Type | Value |
|---|---:|
| True positives | 1 |
| False positives | 0 |
| False negatives | 0 |
| Unlabelled extra findings | 19 |

## 5. Evaluation Metrics

| Metric | Formula | Value |
|---|---|---:|
| Precision | TP / (TP + FP) | 1.0 |
| Recall | TP / (TP + FN) | 1.0 |
| F1 score | 2 × (Precision × Recall) / (Precision + Recall) | 1.0 |

## 6. False Negative Review

No false negatives were found.

## 7. Unlabelled Extra Findings

Checkov also reported additional findings that were not part of the current ground-truth label.

In this early review-mode version of the benchmark, these are stored as **unlabelled extra findings** instead of being counted as false positives.

- `CKV_K8S_20`: Containers should not run with allowPrivilegeEscalation
- `CKV_K8S_11`: CPU limits should be set
- `CKV_K8S_10`: CPU requests should be set
- `CKV_K8S_21`: The default namespace should not be used
- `CKV_K8S_28`: Minimize the admission of containers with the NET_RAW capability
- `CKV_K8S_43`: Image should use digest
- `CKV_K8S_15`: Image Pull Policy should be Always
- `CKV_K8S_8`: Liveness Probe Should be Configured
- `CKV_K8S_13`: Memory limits should be set
- `CKV_K8S_12`: Memory requests should be set
- `CKV_K8S_37`: Minimize the admission of containers with capabilities assigned
- `CKV_K8S_29`: Apply security context to your pods and containers
- `CKV_K8S_9`: Readiness Probe Should be Configured
- `CKV_K8S_22`: Use read-only filesystem for containers where possible
- `CKV_K8S_23`: Minimize the admission of root containers
- `CKV_K8S_40`: Containers should run as a high UID to avoid host conflict
- `CKV_K8S_31`: Ensure that the seccomp profile is set to docker/default or runtime/default
- `CKV_K8S_38`: Ensure that Service Account Tokens are only mounted where necessary
- `CKV2_K8S_6`: Minimize the admission of pods which lack an associated NetworkPolicy

## 8. Interpretation

For this first controlled benchmark case, Checkov correctly detected the intended privileged-container issue.

Because the scanner detected the only ground-truth misconfiguration and did not miss it, recall is 1.0.

Because review mode does not count the extra unmapped findings as false positives yet, precision is also 1.0.

The 19 unlabelled extra findings show that Checkov reports many additional Kubernetes best-practice issues. Later in the project, these findings can either be mapped to new benchmark categories or counted as false positives in a stricter evaluation mode.

## 9. End-to-End Status

This case successfully completed the first mini end-to-end benchmark flow:

artifact.yaml
→ Checkov raw JSON
→ normalised JSON
→ matched JSON
→ metrics JSON
→ markdown report

## 10. Conclusion

The first end-to-end Checkov benchmark test is successful. The system can scan a controlled Kubernetes misconfiguration, normalise the scanner output, match the finding to ground truth, calculate precision, recall and F1, and generate a readable report.
