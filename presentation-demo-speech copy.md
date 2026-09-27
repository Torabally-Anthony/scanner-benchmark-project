## Slide 1: Introduction

*About 20 seconds*

Good day. My name is **[your name]**, and I am an Honours student at the University of Johannesburg. My project asks a practical cloud-security question: if several tools scan the same infrastructure file, how do we fairly compare what they find? I explored this by benchmarking Checkov, Trivy, and Kubescape against IaC such K8s yaml, dockerfiles, and helm charts.

## Slide 2: The problem

*About 30 seconds*

When I compared these tools, I found that they often describe the same issue differently. Each scanner has its own rule IDs, severity ratings, and JSON format. Raw alert totals do not solve this because more findings do not automatically mean better detection. We need a controlled test where the expected answer is already known.

## Slide 3: Research question

*About 20 seconds*

That led to my research question: how accurately and consistently do these scanners detect known misconfigurations in a controlled, labelled corpus? My project adds an evaluation layer around the scanners, giving their different outputs a common meaning that supports fair and repeatable comparison.

## Slide 4: Literature context

*About 20 seconds*

Previous studies show that Infrastructure-as-Code repositories contain real security problems, but scanner results vary widely. Researchers often validate findings manually because the tools do not speak the same language. My work turns that reasoning into a reusable benchmark process.

## Slide 5: Benchmark design

*About 30 seconds*

The process begins with a deliberately insecure artifact and a written description of the expected issue. I run the applicable scanners and map their equivalent rule IDs to that issue. The pipeline then converts their outputs into one format, matches the findings to the ground truth, calculates metrics, and generates reports. Manual preparation establishes the meaning, while automation makes the test repeatable.

## Slide 6: Corpus and coverage

*About 25 seconds*

This slide shows the original alpha corpus of six cases. The current prototype has grown to 60 cases, with 20 in each artifact family, giving us 160 applicable evaluations. Kubescape is excluded from Dockerfiles because it does not scan that artifact type.

## Slide 7: Ground truth and normalisation

*About 30 seconds*

The ground-truth file records the expected issue, where it appears, and what the secure alternative should be. Scanner IDs then act as translations. For example, take the use case privileged-container case, Checkov uses `CKV_K8S_16`, Trivy uses `KSV-0017`, and Kubescape uses `C-0057`. Normalisation connects all three to the same label while preserving the original result.

## Slide 8: Matching and metrics

*About 25 seconds*

Once the findings share a common format, the system applies strict matching. A correct match is a true positive, while a missed issue becomes a false negative. A finding without a ground-truth mapping counts as a false positive within this benchmark. These counts produce precision, recall, and F1.

## Slide 9: Example result

*About 35 seconds*

This result shows why that distinction matters. All three scanners found the privileged-container issue, so they achieved perfect recall. Their precision was low because they also reported many unmapped findings. Trivy had the best F1 here because it produced fewer of them. Those extra warnings are not necessarily incorrect. They simply fall outside this case's label, which shows why complete ground truth matters.

## Transition to the browser

*Switch to the browser after slide 9. Keep slide 10 for the end.*

Now that I have explained the method, I will follow that same privileged-container case through the prototype so you can see how a user moves from a test case to a final comparison.

## Browser demonstration

### Dashboard

*Begin on the Dashboard. About 25 seconds.*

The dashboard confirms that the backend is connected and summarises the experiment: 60 cases, divided evenly across the three artifact families, and 160 applicable results. The menu follows the same stages as the research method.

### Benchmark Corpus

*Click **Benchmark Corpus**. About 25 seconds.*

The corpus page shows what the scanners are tested against. Here is the privileged-container case, labelled `GT-001`, along with its severity and applicable scanners. All three tools support this Kubernetes case. For Dockerfiles, the system correctly leaves out Kubescape.

### Process Benchmark

*Click **Process Benchmark**. About 25 seconds.*

On the processing page, I choose a case and the scanners to evaluate. The dashboard takes their saved raw JSON through normalisation, matching, metric calculation, and reporting. I will use the existing results so we can focus on the output.

### Normalised Findings

*Click **Normalised Findings**, keep the first case and Checkov selected, and click **Load output**. About 30 seconds.*

After normalisation, Checkov's original JSON appears in the shared schema. It reported 20 findings for this case. One maps to the intended issue and 19 remain unmapped. The next stage can now treat every scanner consistently.

### Matching Results

*Click **Matching Results**, then click **Load output**. About 30 seconds.*

The matching view explains the numbers. Checkov rule `CKV_K8S_16` maps to `GT-001`, giving one true positive. The other 19 findings have no mapping in this case, so strict matching classifies them as false positives. Each result remains available for inspection.

### Per-Case Metrics

*Click **Per-Case Metrics**. About 25 seconds.*

The metrics page compares all three scanners for this case. Each found the intended issue, so recall is one. Their F1 scores differ because Checkov produced 19 unmapped findings, Trivy 17, and Kubescape 22. This comparison says more than raw alert totals.

### Comparison Report

*Click **Comparison Report**. About 40 seconds.*

The comparison report moves from one case to the full corpus. Trivy achieved the strongest overall balance, with a micro F1 of 42.92 percent. Checkov reached 31.97 percent. Kubescape had the highest recall across its 40 applicable cases, but its many unmapped findings reduced its micro F1 to 17.74 percent. Because Kubescape does not cover Dockerfiles, its total is not directly equivalent to the other two.

## Slide 10: Conclusion

*Return to slide 10. About 40 seconds.*

Bringing this back to the research question, the prototype shows that different scanner outputs can be compared consistently. Semantic mapping connects their rule systems to one ground truth, while the pipeline keeps every metric traceable to the original finding.

The experiment also shows that benchmark design matters. Incomplete labels can make useful extra warnings appear as false positives. Trivy provides the strongest overall balance in this corpus, although the right scanner still depends on the artifact type and the user's priorities. The expansion from six to 60 cases also shows that the approach can scale. Thank you.

## Recording preparation

1. Start the application from the project root:

   ```bash
   .venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
   ```

2. Open `http://127.0.0.1:8000/` and wait for the dashboard totals to load.
3. Keep the browser on the Dashboard and the presentation on slide 1.
4. After slide 9, switch to the browser and follow the navigation cues above.
5. Return to slide 10 after the Comparison Report.
6. Use the saved results during the recording. This avoids waiting for processing and keeps the demonstration predictable.
7. Focus on **micro F1** in the comparison. The current macro calculation can overstate performance when a case has an undefined F1 score.
