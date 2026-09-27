# Cloud-Native Scanner Benchmark Presentation and Demo Speech

**Target duration:** 5 to 8 minutes  
**Source slides:** `/Users/anthonytorabally/Desktop/workspace/UJ/D08/final-d08.pdf`

Present slides 1 through 9, move to the browser for the practical demonstration, and return to slide 10 for the conclusion. Italic text contains recording cues and should not be read aloud.

## Slide 1: Introduction

*About 15 seconds.*

Good day. My name is **[your name]**, and I am an Honours student at the University of Johannesburg. My project asks a practical cloud-security question: if different tools scan the same infrastructure file, how can we compare them fairly?

## Slide 2: The problem

*About 20 seconds.*

Checkov, Trivy, and Kubescape use different rule IDs, severity labels, and JSON formats. This makes raw alert totals misleading, because reporting more findings does not necessarily mean that a scanner detected the issue we intended to test.

## Slide 3: Research question

*About 15 seconds.*

My research question is: how accurately and consistently do these scanners detect known misconfigurations in a controlled, labelled corpus? The expected result is defined before the scanner is evaluated.

## Slide 4: Literature context

*About 15 seconds.*

Previous research shows that Infrastructure-as-Code contains real security problems, but scanner results often disagree and require manual validation. This project turns that validation into a repeatable process.

## Slide 5: Benchmark design

*About 25 seconds.*

Each test case contains a deliberately insecure artifact and a ground-truth description of its issue. The applicable scanners analyse it, and the pipeline normalises their outputs, maps equivalent rules to the ground truth, classifies the findings, calculates metrics, and generates reports.

## Slide 6: Corpus and coverage

## Slide 7: Ground truth and normalisation

*About 20 seconds.*

Ground truth records the expected issue and affected resource. A mapping file translates each scanner’s rule into that shared meaning. For the privileged-container case, Checkov uses `CKV_K8S_16`, Trivy uses `KSV-0017`, and Kubescape uses `C-0057`.

## Slide 8: Matching and metrics

*About 15 seconds.*

Once the findings have a shared format, the system classifies true positives, false positives, and false negatives. These counts produce precision, recall, and F1. I will explain them using a real result in the demonstration.

## Slide 9: Example result

*About 15 seconds.*

All three scanners found this privileged-container issue, but they returned different numbers of additional findings. Their recall is therefore equal, while their precision and F1 differ. Let me show how the prototype reaches that result.

## Transition to the browser

*Switch from slide 9 to the browser. Keep slide 10 for the conclusion.*

I will follow that privileged-container case from its ground truth to the final comparison.

## Practical prototype demonstration

### Dashboard

*Begin on the Dashboard. Point to the summary cards, metric cards, and quick actions.*

This dashboard confirms that the backend is connected and summarises the experiment: 60 cases across three artifact families and 160 applicable evaluations.

These metric cards explain how performance is measured. **Precision** is the proportion of benchmark-classified findings that are true positives. **Recall** is the proportion of known issues that the scanner successfully detects. **F1** balances precision and recall, so it rewards detection without ignoring unnecessary findings.

The buttons below are shortcuts: **Review corpus** opens the test cases, **Process results** opens the pipeline, and **Open comparison** and **Open reports** open the final outputs. **Refresh data** reloads the latest saved information.

### Benchmark Corpus

*Click **Benchmark Corpus** and point to `case-001-privileged-container`.*

The corpus shows what the scanner is tested against. This case is linked to ground-truth ID `GT-001`, its severity, and its applicable scanners. 

### Process Benchmark

*Click **Process Benchmark**. Select `case-001-privileged-container` and show the scanner checkboxes.*

Here I choose a case and its scanners. Unsupported choices are disabled automatically; Kubescape, for example, is unavailable for Dockerfiles.

**Process selected scanners** takes existing raw JSON through normalisation, matching, metrics, and report generation. The progress bar and result cards show what happened, while **Full processing log** exposes the underlying diagnostic output. **Load saved results** retrieves completed metrics without rerunning the pipeline, which I will use for this demonstration.

### Raw Scanner Outputs

*Click **Raw Outputs**. Select the privileged-container case and **Trivy**, then click **Load output**.*

The case, scanner, and stage controls identify the exact file to retrieve. **Load output** now shows Trivy’s original JSON. It is useful as evidence, but it cannot yet be compared directly with the other scanners’ differently structured output.

### Normalised Findings

*Click **Normalised Findings**, then **Load output**.*

Normalisation converts that JSON into the shared schema. Trivy produced 18 findings: `KSV-0017` maps to `GT-001`, while 17 are unmapped for this case. The cards retain the original rule and severity, and **Full normalised JSON** exposes the complete record.

### Matching Results

*Click **Matching Results**, then **Load output**. Point to TP, FP, and FN.*

This is where the classifications become practical. A **true positive**, or TP, is a finding that matches the expected issue. Trivy’s `KSV-0017` matches `GT-001`, giving one TP.

A **false positive**, or FP, is a finding without a ground-truth mapping in this strict case, giving Trivy 17 FPs. Those warnings are not necessarily wrong in the real world; they are simply outside this case’s label. A **false negative**, or FN, is an expected issue that was missed. Trivy has zero because it found the privileged-container issue.

### Per-Case Metrics

*Click **Per-Case Metrics**, keep the same case selected, and click the Trivy row.*

Those counts now explain the scores. Precision is TP divided by TP plus FP, so Trivy scores one divided by 18, or 5.56 percent. Recall is TP divided by TP plus FN, so it scores 100 percent. F1 balances the two and is 10.53 percent.

All three scanners have perfect recall for this case. Trivy has the best F1 because it returned 17 unmapped findings, compared with Checkov’s 19 and Kubescape’s 22. Clicking a scanner row updates the cards above.

### Reports

*Click **Reports** and open Trivy’s report for `case-001-privileged-container`. Expand **Full report**.*

The per-case report explains where that score came from. It records the scanner version and run status, then lists 18 normalised findings, one ground-truth issue, one TP, 17 FPs, and zero FNs. It also shows the formulas, confirms that `GT-001` was detected by `KSV-0017`, previews the classified findings, and points to the full matched and metric files. **Reload reports** refreshes the available report list.

### Comparison Report

*Click **Comparison Report**. Point to the buttons, overall table, coverage matrix, and results-by-family table.*

This page combines all applicable results. **Reload comparison** reads the existing aggregate, while **Generate comparison** rebuilds it from the latest per-case metrics.

Checkov covers all 60 cases, with 43 TPs, 166 FPs, and 17 FNs, producing a micro F1 of 31.97 percent. Trivy also covers all 60, but improves those counts to 47 TPs, 112 FPs, and 13 FNs. Its micro F1 is 42.92 percent—the strongest overall balance—making Trivy the better general pick for this corpus.

Kubescape covers 40 cases because its 20 Dockerfile results are correctly marked **Not applicable**. Its recall is the highest at 82.5 percent, but 299 FPs reduce its precision to 9.94 percent and its micro F1 to 17.74 percent. It finds many expected issues, but its results require more filtering.

The coverage matrix shows each result as **Detected**, **Missed**, or **Not applicable**. The family table explains the wider pattern. Dockerfiles score highest: Trivy reaches 94.74 percent micro F1 and Checkov 66.67 percent. Kubernetes sits in the middle, led by Trivy at 40 percent. Helm scores lowest for every applicable scanner: Trivy reaches 27.03 percent, Checkov 24.11 percent, and Kubescape 15.67 percent. Helm still has good recall, but its many unmapped findings lower precision and F1.

I focus on micro F1 because it pools the TP, FP, and FN counts. The final per-case table keeps those overall results traceable to every scanner and case.

## Slide 10: Conclusion

*Return to slide 10. About 25 seconds.*

To conclude, the prototype creates one traceable comparison from three different scanner formats. Ground truth defines what should be found, matching explains TP, FP, and FN, and the reports connect those classifications to precision, recall, and F1.

Trivy offers the best overall balance in this corpus. Dockerfiles produced the strongest results, while Helm produced the weakest because of its many unmapped findings. This shows why artifact support, detection coverage, and precision matter more than alert totals alone. Thank you.

## Recording preparation

1. Start the application from the project root:

   ```bash
   .venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
   ```

2. Open `http://127.0.0.1:8000/` and wait for the dashboard totals to load.
3. Keep the browser on the Dashboard and the presentation on slide 1.
4. Confirm that `case-001-privileged-container` and Trivy load in Raw, Normalised, Matched, Metrics, and Reports before recording.
5. Use saved results instead of running a new process during the recording.
6. Follow this path: **Dashboard → Benchmark Corpus → Process Benchmark → Raw Outputs → Normalised Findings → Matching Results → Per-Case Metrics → Reports → Comparison Report**.
7. Return to slide 10 after the Comparison Report.
8. Focus on **micro F1** in the combined comparison because it pools all TP, FP, and FN counts across applicable cases.
