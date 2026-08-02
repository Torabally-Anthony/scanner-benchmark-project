# Case 001 Trivy Benchmark Report

## 1. Case Summary

- Case ID: `case-001-privileged-container`
- Scanner: `trivy`
- Artifact type: `kubernetes_yaml`
- Benchmark issue: Privileged container
- Ground truth ID: `GT-001`

## 2. Ground Truth Detection Result

- Ground truth items: `1`
- Normalised Trivy findings: `18`
- Mapped findings: `1`
- Unmapped findings: `17`

## 3. True Positive Findings

- Ground truth: `GT-001`
  - Scanner rule: `KSV-0017`
  - Rule name: Privileged
  - Resource: `Deployment.default.privileged-demo-app`
  - Container: `demo-container`
  - Field path: `spec.template.spec.containers[0].securityContext.privileged`
  - Evidence: Container 'demo-container' of Deployment 'privileged-demo-app' should set 'securityContext.privileged' to false

## 4. False Negative Review

No false negatives were found. Trivy detected the labelled ground-truth issue.

## 5. Metric Counts

- True positives: `1`
- False positives: `0`
- False negatives: `0`
- Unlabelled extra findings: `17`

## 6. Evaluation Metrics

- Precision: `1.0`
- Recall: `1.0`
- F1 score: `1.0`

## 7. Unlabelled Extra Findings

These findings were reported by Trivy but are not counted as false positives yet because the benchmark is currently using review mode.

- `KSV-0001` — Can elevate its own privileges (Medium)
- `KSV-0003` — Default capabilities: some containers do not drop all (Low)
- `KSV-0004` — Default capabilities: some containers do not drop any (Low)
- `KSV-0011` — CPU not limited (Low)
- `KSV-0012` — Runs as root user (Medium)
- `KSV-0014` — Root file system is not read-only (High)
- `KSV-0015` — CPU requests not specified (Low)
- `KSV-0016` — Memory requests not specified (Low)
- `KSV-0018` — Memory not limited (Low)
- `KSV-0020` — Runs with UID <= 10000 (Low)
- `KSV-0021` — Runs with GID <= 10000 (Low)
- `KSV-0030` — Runtime/Default Seccomp profile not set (Low)
- `KSV-0104` — Seccomp policies disabled (Medium)
- `KSV-0106` — Container capabilities must only include NET_BIND_SERVICE (Low)
- `KSV-0110` — Workloads in the default namespace (Low)
- `KSV-0117` — Prevent binding to privileged ports (Medium)
- `KSV-0118` — Default security context configured (High)

## 8. Interpretation

Trivy successfully detected the privileged container misconfiguration using rule `KSV-0017`. This finding matched the ground truth label `GT-001`, so it was classified as a true positive.

The additional Trivy findings were stored as unlabelled extras. They may represent valid security recommendations, but they are not part of the current ground-truth label set for this controlled benchmark case.

## 9. Conclusion

The first Trivy benchmark run was successful. For case-001, Trivy detected the intended privileged container issue, producing Precision = 1.0, Recall = 1.0, and F1 Score = 1.0 in review mode.
