# Benchmarking Cloud-Native Misconfiguration Scanners

## Reworked presentation and live-demo speech

**Estimated duration:** 10 to 12 minutes, including interface interactions  
**Main demonstration case:** `case-001-privileged-container`  
**Secondary processing example:** `case-002-runs-as-root`  

Text in *italics* describes what should happen on screen and should not be read aloud. The wording is intentionally conversational so it can be recorded naturally.

> **Important recording note:** The current Process Benchmark interface selects one case per run. To demonstrate more than one case, the recording will switch cases and run them sequentially. It can run one scanner or several scanners for the selected case.

---

## Slide 1 - Introduction

*Show the title slide.*

Good day. My name is **[your name]**, and I am an Honours student at the University of Johannesburg. This project looks at a practical cloud-security problem: when different scanners inspect the same infrastructure file, how do we decide which result is genuinely useful?

## Slide 2 - The problem

*Move to the problem slide.*

Checkov, Trivy, and Kubescape can scan the same artifact and still produce very different outputs. They use different rule identifiers, JSON structures, severity labels, and reporting styles. Because of that, simply counting alerts does not give us a fair comparison. A scanner can produce more warnings while still missing the specific issue being tested.

## Slide 3 - Benchmark design

*Move to the benchmark-design slide. Briefly highlight 60 cases, the three artifact families, and 160 applicable scanner-case results.*

To make the comparison controlled, I built a corpus of 60 deliberately insecure use cases. It contains 20 Kubernetes YAML cases, 20 Dockerfile cases, and 20 Helm cases. Each case has its own labelled ground truth, which defines the issue that the scanner is expected to find. There are 160 applicable scanner-case results because Kubescape is not evaluated against Dockerfiles.

## Slide 4 - Evaluation pipeline

*Move across the pipeline from raw output to reporting.*

Every result follows the same evaluation path. The system keeps the original scanner JSON as evidence, converts it into a common schema, matches the scanner's rule identifiers to the ground truth, calculates true positives, false positives, and false negatives, and then produces metrics and readable reports. This gives us a traceable result instead of an unsupported score.

## Slide 5 - Transition to the prototype

*Show the prototype slide, then switch to the browser.*

I will now demonstrate that complete journey in the prototype. I will begin with the corpus, process a real benchmark case, inspect each output stage, and finish with the combined scanner comparison.

---

# Live prototype demonstration

## Dashboard

*Begin at the top of the Dashboard. Highlight **Backend connected**, then the five overview values.*

The green backend indicator confirms that the browser is communicating with the FastAPI service. The overview then shows the scale of the current experiment: 60 cases in total, divided evenly between Kubernetes YAML, Dockerfiles, and Helm charts. The final figure is 160 scanner-case results. That number includes only applicable combinations, so Kubescape's lack of Dockerfile support does not count against it.

*Scroll to the Quick actions panel. Move the pointer across each action while it is mentioned.*

The Quick actions provide shortcuts into the main workflow. Review corpus opens the labelled test cases. Process results opens the analysis pipeline. Open comparison goes to the corpus-wide tables, and Open reports displays the generated Markdown reports.

*Scroll to **Selected-case scanner comparison**. Open the case dropdown, choose `case-001-privileged-container`, and highlight the three scanner rows.*

The selected-case comparison gives a quick view of saved results for one use case. For the privileged-container case, all three scanners detected the expected issue, so each has one true positive and zero false negatives. Their false-positive counts differ, which is why their precision and F1 scores also differ. I will build up to these values from the raw output.

## Benchmark Corpus

*Open **Benchmark Corpus**. Highlight the total number of rows by scrolling through the table, then return to `case-001-privileged-container`.*

The corpus page lists all 60 controlled use cases. Each row identifies the artifact family, the independent ground-truth ID, the expected misconfiguration, its severity, and the scanners that apply to it.

*Highlight the first row and select the text `GT-001`, `High`, and the applicable scanner names.*

For this example, `case-001-privileged-container` maps to ground-truth ID `GT-001`. Its severity is High, and Checkov, Trivy, and Kubescape are all applicable. The ground-truth ID is important because it gives the three scanners one shared target even though they use different rule names.

## Process Benchmark

*Open **Process Benchmark**. Open the benchmark-case dropdown and scroll through Kubernetes, Dockerfile, and Helm options before selecting `case-002-runs-as-root`.*

The benchmark dropdown contains the configured cases from all three artifact families. The current interface processes one case per run. If I want to evaluate several cases, I change this selection and process them one after another.

*Select only **Trivy**. Clear the other scanner checkboxes, then click **Process selected scanners**. Show the progress bar and completed Trivy summary.*

For a single-scanner run, I select the case, choose only Trivy, and start the process. The system takes the existing raw JSON through normalisation, ground-truth matching, metric calculation, and report generation. The summary confirms whether the pipeline completed and shows the resulting TP, FP, FN, precision, recall, and F1 values.

*Change the case to `case-001-privileged-container`. Select Checkov, Trivy, and Kubescape. Click **Process selected scanners** and remain on the page while it runs.*

Now I will switch back to the privileged-container case and select all three applicable scanners. This demonstrates that the same case can be processed against one scanner or several scanners in a single request.

*As the run finishes, highlight the three completed cards and their TP, FP, FN, precision, recall, and F1 values.*

The completed summary makes the first comparison immediately visible. Checkov produces one true positive, 19 false positives, and no false negatives. Trivy produces one true positive, 17 false positives, and no false negatives. Kubescape also finds the issue, but it has 22 false positives. All three detect the target, while Trivy returns the fewest additional unmapped findings for this case.

*Expand **Full processing log**. Slowly scroll from the top to the bottom, pausing at the header, the four stages for at least one scanner, output paths, and the final stage table.*

The full processing log shows how the summary was produced. At the top, it records the case, matching mode, and selected scanner. Each scanner then has four ordered stages: normalisation, ground-truth matching, metrics calculation, and report generation.

For every stage, the log shows the command that ran, whether it passed, and the output that it created. The normalisation section reports how many findings were mapped or left unmapped. The matching section gives the TP, FP, and FN counts. The metrics section prints precision, recall, and F1, and the reporting section shows where the Markdown report was saved.

At the bottom, the pipeline summary places every scanner and stage into one status table with its execution time. This makes the interface useful for both presentation and diagnosis: the cards explain the result, while the log shows exactly how the system reached it.

## Raw Outputs

*Open **Raw Outputs**. Keep `case-001-privileged-container` selected.*

The raw-output page lets me choose a case and scanner, then retrieve the original machine-readable result. I will load the same case for all three scanners so that their structural differences are visible.

*Choose **Checkov**, click **Load output**, highlight the header and the `results` and `summary` areas, and scroll briefly.*

Checkov organises its result around a summary and lists of passed and failed checks.

*Choose **Trivy**, click **Load output**, highlight `Results` and `Misconfigurations`, and scroll briefly.*

Trivy uses a different hierarchy, with artifact metadata followed by results and misconfiguration objects.

*Choose **Kubescape**, click **Load output**, highlight `resources`, `results`, and `summaryDetails`, and scroll briefly.*

Kubescape has another structure again, organised around resources, controls, and summary details. These files are valuable as evidence, but their different schemas make direct comparison unreliable. That is why the next stage is necessary.

## Normalised Findings

*Open **Normalised Findings**. Keep the same case selected. Load Checkov, Trivy, and Kubescape one after another. For each scanner, highlight the total, mapped, and unmapped counts, then the mapped rule card.*

The normalised page converts each scanner's JSON into one common finding model. Checkov produces 20 findings: one mapped and 19 unmapped. Its rule `CKV_K8S_16` maps to `GT-001`.

Trivy produces 18 findings: one mapped and 17 unmapped. Its equivalent rule is `KSV-0017`.

Kubescape produces 23 findings: one mapped and 22 unmapped. Its rule `C-0057` maps to the same ground truth.

The rule identifiers are different, but the common schema preserves their meaning, severity, resource, mapping status, and original scanner details. The expandable full JSON remains available when deeper inspection is needed.

## Matching Results

*Open **Matching Results**. Load the same case for Checkov, Trivy, and Kubescape. Highlight the TP, FP, and FN counters and the mapped rule for each scanner. Expand a few remaining findings where useful.*

The matching page classifies the normalised findings against the labelled ground truth. A true positive, or TP, is a scanner finding that maps to the expected issue. That gives Checkov's `CKV_K8S_16`, Trivy's `KSV-0017`, and Kubescape's `C-0057` one true positive each.

A false positive, or FP, is a finding without a mapping in this strict, single-issue case. Checkov has 19, Trivy has 17, and Kubescape has 22. Those warnings are not automatically meaningless in a real environment. They count as false positives here because this controlled case labels only the privileged-container issue.

A false negative, or FN, would mean that the expected issue was not detected. All three scanners have zero false negatives for this case, so they all achieve full recall.

## Per-Case Metrics

*Open **Per-Case Metrics**, select `case-001-privileged-container`, then click each scanner row in turn so the three cards update. Highlight each card as it is explained.*

The metrics page turns those classification counts into comparable scores. Precision asks how many reported findings were true positives, so it falls when false positives increase. Recall asks how many expected issues were detected, so all three scanners score one, or 100 percent, on this case. F1 combines precision and recall into one balanced value.

The scanner comparison table controls the cards above it. Clicking Checkov shows precision of 0.05, recall of 1.00, and F1 of about 0.10. Trivy improves slightly to precision of 0.06 and F1 of about 0.11 because it has fewer false positives. Kubescape has precision of 0.04 and F1 of about 0.08. The cards therefore explain the selected row rather than showing an unexplained overall score.

## Reports

*Open **Reports**. Select Trivy's report for `case-001-privileged-container`. Highlight the summary, then expand **Full report** and scroll through its sections.*

The reports page turns the saved evaluation into a readable record. The summary confirms one TP, 17 FPs, zero FNs, and the resulting precision, recall, and F1 values for Trivy.

The full report adds the context behind those numbers. It identifies the scanner version and evaluation mode, shows the result counts and formulas, confirms that `GT-001` was detected by `KSV-0017`, and previews both the true-positive and false-positive findings. It also links the result back to the complete matched and metrics files, which keeps the score auditable.

## Comparison Report

*Open **Comparison Report**. Begin at **Overall scanner summary** and highlight the Trivy row.*

The comparison page combines the saved metrics across the corpus. The overall scanner summary pools all applicable cases. Trivy has the strongest overall micro F1 at 42.92 percent, compared with 31.97 percent for Checkov and 17.74 percent for Kubescape. Trivy also has more true positives and fewer false positives than Checkov across the full corpus, giving it the best overall balance in this benchmark.

*Scroll to **Scanner coverage matrix**. Pause on early Kubernetes cases, then scroll to a Dockerfile section and highlight Kubescape's Not applicable entries.*

The coverage matrix answers a simpler question for every case: was the expected issue detected, missed, or not applicable? It makes individual gaps easy to locate. It also shows Kubescape as not applicable for Dockerfiles rather than incorrectly treating unsupported scans as failures.

*Scroll to **Results by artifact family**. Highlight the Dockerfile rows, then the Helm rows.*

The artifact-family table explains where scanner performance changes. Dockerfiles produce the strongest results. Trivy reaches a micro F1 of 94.74 percent, while Checkov reaches 66.67 percent. Helm produces the lowest scores for every applicable scanner: 27.03 percent for Trivy, 24.11 percent for Checkov, and 15.67 percent for Kubescape. The Helm scanners still detect many expected issues, but their larger numbers of unmapped findings reduce precision and F1.

*Scroll to **Per-case comparison** and locate the three `case-001-privileged-container` rows.*

Finally, the per-case table keeps the aggregate findings traceable. I can return to the privileged-container case and see the exact TP, FP, FN, precision, recall, and F1 result for each scanner. This is the detailed evidence behind the overall and artifact-family summaries.

---

## Slide 6 - Conclusion

*Return to the presentation and show the final slide.*

To conclude, this prototype provides a controlled path from three incompatible scanner formats to one comparable result. Ground truth defines what should be detected, rule mapping connects equivalent findings, and the reports preserve the evidence behind every score.

Within this corpus, Trivy provides the strongest overall F1 balance. Dockerfiles achieve the highest family-level results, while Helm has the lowest because of its larger number of unmapped findings. The main finding is that scanner quality cannot be judged by alert totals alone. It must be evaluated against known issues, applicable artifact types, and the cost of additional findings. Thank you.

---

## Screen-recording route

1. Slides 1 to 5.
2. Dashboard.
3. Benchmark Corpus.
4. Process Benchmark: one Trivy run on `case-002-runs-as-root`, then all three scanners on `case-001-privileged-container`.
5. Raw Outputs: Checkov, Trivy, Kubescape.
6. Normalised Findings: Checkov, Trivy, Kubescape.
7. Matching Results: Checkov, Trivy, Kubescape.
8. Per-Case Metrics: click all three scanner rows.
9. Reports: open and expand the Trivy report for `case-001-privileged-container`.
10. Comparison Report: overall summary, coverage matrix, artifact-family table, and per-case table.
11. Return to slide 6.

## Pronunciation guide

- **Trivy:** TRY-vee
- **Kubescape:** KUBE-escape
- **Checkov:** CHECK-ov
- **IaC:** say “eye-ay-see” or “Infrastructure as Code”
- **F1:** say “F-one”

