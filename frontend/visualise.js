"use strict";

// Charts use the same saved report as the comparison tables. No scores are
// recalculated here: undefined metrics remain distinct from real zero scores.
const BenchmarkVisualise = (() => {
  const chartColors = {
    truePositive: "#57d879",
    falseNegative: "#8a0303",
    falsePositive: "#faf0be",
    precision: "#38bdf8",
    recall: "#4f46e5",
    f1: "#4b1f6f",
  };
  const scoreSeries = [
    { key: "micro_precision", label: "Precision", color: chartColors.precision },
    { key: "micro_recall", label: "Recall", color: chartColors.recall },
    { key: "micro_f1_score", label: "F1", color: chartColors.f1 },
  ];
  const findingSeries = [
    { key: "true_positive_count", label: "True positives", color: chartColors.truePositive },
    { key: "false_positive_count", label: "False positives", color: chartColors.falsePositive },
    { key: "false_negative_count", label: "False negatives", color: chartColors.falseNegative },
  ];
  const scannerColors = {
    checkov: "#f08080",
    trivy: "#77bdf2",
    kubescape: "#b79ced",
  };
  const outcomeSeries = [
    { key: "detected", label: "Detected", color: chartColors.truePositive },
    { key: "partial", label: "Partial", color: chartColors.falsePositive },
    { key: "missed", label: "Missed", color: chartColors.falseNegative },
    { key: "no labelled result", label: "No labelled result", color: "#8090a5" },
    { key: "unavailable", label: "No result", color: "#c5cdd8" },
  ];

  function numeric(value) {
    return typeof value === "number" && Number.isFinite(value) && value >= 0
      ? value : null;
  }

  function percent(value) {
    return numeric(value) === null ? "—" : `${(value * 100).toFixed(1)}%`;
  }

  function count(value) {
    return numeric(value) === null ? "—" : value.toLocaleString();
  }

  function swatch(color) {
    return `<span class="visualise-swatch" style="--chart-color:${color}" aria-hidden="true"></span>`;
  }

  function legend(series) {
    return `<div class="visualise-legend">${series.map(item =>
      `<span>${swatch(item.color)}${escapeHtml(item.label)}</span>`).join("")}</div>`;
  }

  function axis(max, asPercent) {
    return `<div class="visualise-axis" aria-hidden="true"><span>0${asPercent ? "%" : ""}</span>
      <span>${asPercent ? "50%" : count(max / 2)}</span><span>${asPercent ? "100%" : count(max)}</span></div>`;
  }

  function bar(label, value, color, max = 1, asPercent = true) {
    const valid = numeric(value) !== null;
    const width = valid ? Math.min(100, value / max * 100) : 0;
    return `<div class="visualise-bar-row">
      <span class="visualise-bar-label">${escapeHtml(label)}</span>
      <span class="visualise-track" aria-hidden="true"><span class="visualise-bar" style="width:${width}%;--chart-color:${color}"></span></span>
      <strong class="visualise-value"${valid ? "" : ' title="Undefined in the report"'}>${asPercent ? percent(value) : count(value)}</strong>
    </div>`;
  }

  function unavailable(report, artifact, scanner) {
    const applicable = report.corpus_summary?.[artifact]?.applicable_scanners;
    return artifact !== "all" && Array.isArray(applicable) && !applicable.includes(scanner)
      ? "Not applicable" : "No results in this selection";
  }

  function scannerCharts(report, artifact, summaries) {
    const maximum = Math.max(0, ...Object.values(summaries).flatMap(summary =>
      findingSeries.map(series => numeric(summary[series.key]) ?? 0)));
    // A shared count axis always starts at zero, with a readable even endpoint.
    const countMax = Math.max(2, Math.ceil(maximum / 2) * 2);

    for (const [id, series, isScore] of [
      ["visualiseScores", scoreSeries, true],
      ["visualiseFindings", findingSeries, false],
    ]) {
      $(id).innerHTML = legend(series) + axis(isScore ? 1 : countMax, isScore)
        + SCANNERS.map(scanner => {
          const summary = summaries[scanner];
          const hasCases = numeric(summary?.applicable_case_count) > 0;
          return `<div class="visualise-group">
            <div class="visualise-group-title"><strong>${escapeHtml(scannerName(scanner))}</strong>
              <span>${hasCases ? `${count(summary.applicable_case_count)} applicable cases` : unavailable(report, artifact, scanner)}</span></div>
            ${hasCases ? series.map(item => bar(item.label, summary[item.key], item.color, isScore ? 1 : countMax, isScore)).join("") : ""}
            ${hasCases && !isScore ? `<p class="visualise-extra">Unlabelled extras: ${count(summary.unlabelled_extra_findings_count)}</p>` : ""}
          </div>`;
        }).join("");
    }
  }

  function detectionChart(report, artifact) {
    const scanner = $("visualiseScanner").value;
    const rows = (report.coverage_matrix ?? []).filter(row => artifact === "all" || row.artifact_type === artifact);
    const totals = Object.fromEntries(outcomeSeries.map(item => [item.key, 0]));
    let excluded = 0;
    rows.forEach(row => {
      const status = String(row.scanners?.[scanner] ?? "unavailable").toLowerCase();
      if (status === "not applicable") {
        excluded += 1;
      } else {
        totals[Object.hasOwn(totals, status) ? status : "unavailable"] += 1;
      }
    });
    const total = Object.values(totals).reduce((sum, value) => sum + value, 0);
    if (!total) {
      $("visualiseDetection").innerHTML = `<div class="visualise-chart-empty">${escapeHtml(unavailable(report, artifact, scanner))}.</div>`;
      return;
    }

    let offset = 0;
    const segments = outcomeSeries.map(item => {
      const length = totals[item.key] / total * 100;
      const segment = length ? `<circle cx="100" cy="100" r="76" pathLength="100"
        fill="none" stroke="${item.color}" stroke-width="23"
        stroke-dasharray="${length} ${100 - length}" stroke-dashoffset="${-offset}"
        transform="rotate(-90 100 100)" />` : "";
      offset += length;
      return segment;
    }).join("");

    $("visualiseDetection").innerHTML = `<div class="visualise-detection">
      <div class="visualise-ring">
        <svg viewBox="0 0 200 200" aria-hidden="true">${segments}</svg>
        <div class="visualise-ring-label"><strong>${count(total)}</strong><span>applicable cases</span></div>
      </div>
      <ul class="visualise-outcomes" aria-label="${escapeHtml(scannerName(scanner))} case detection outcomes">
        ${outcomeSeries.filter(item => totals[item.key] > 0 || ["detected", "partial", "missed"].includes(item.key)).map(item =>
          `<li><span>${swatch(item.color)}${item.label}</span><strong>${count(totals[item.key])}</strong><span>${percent(totals[item.key] / total)}</span></li>`).join("")}
      </ul>
    </div><p class="visualise-note">${count(excluded)} not-applicable cases excluded. Case counts are for ${escapeHtml(scannerName(scanner))} only.</p>`;
  }

  function familyChart(report, artifacts) {
    $("visualiseFamilies").innerHTML = legend(SCANNERS.map(scanner => ({
      label: scannerName(scanner), color: scannerColors[scanner],
    }))) + axis(1, true) + artifacts.map(([artifact, family]) =>
      `<div class="visualise-group">
        <div class="visualise-group-title"><strong>${escapeHtml(family.label ?? artifactName(artifact))}</strong><span>${count(family.case_count)} cases</span></div>
        ${SCANNERS.map(scanner => {
          const summary = report.artifact_summaries?.[artifact]?.scanners?.[scanner];
          return numeric(summary?.applicable_case_count) > 0
            ? bar(scannerName(scanner), summary.micro_f1_score, scannerColors[scanner])
            : `<div class="visualise-unavailable"><span>${escapeHtml(scannerName(scanner))}</span><span>${unavailable(report, artifact, scanner)}</span></div>`;
        }).join("")}
      </div>`).join("");
  }

  function render(report) {
    if (!report) return;
    const artifactSelect = $("visualiseArtifact");
    const previousArtifact = artifactSelect.value;
    const artifacts = Object.entries(report.corpus_summary ?? {}).filter(([, family]) => numeric(family.case_count) > 0);
    artifactSelect.innerHTML = '<option value="all">All artifacts</option>' + artifacts.map(([type, family]) =>
      `<option value="${escapeHtml(type)}">${escapeHtml(family.label ?? artifactName(type))}</option>`).join("");
    artifactSelect.value = artifacts.some(([type]) => type === previousArtifact) ? previousArtifact : "all";
    artifactSelect.disabled = !artifacts.length;

    const scannerSelect = $("visualiseScanner");
    const previousScanner = scannerSelect.value;
    scannerSelect.innerHTML = SCANNERS.map(scanner => `<option value="${scanner}">${scannerName(scanner)}</option>`).join("");
    scannerSelect.value = SCANNERS.includes(previousScanner) ? previousScanner : SCANNERS[0];

    $("visualise").setAttribute("aria-busy", "false");
    $("visualiseStatus").textContent = `Report generated ${dateText(report.generated_at_utc ?? report.updated_at)} · Use Refresh data to reload.`;
    $("visualiseEmpty").hidden = artifacts.length > 0;
    $("visualiseContent").hidden = !artifacts.length;
    if (!artifacts.length) {
      $("visualiseEmpty").textContent = "This comparison report has no cases to visualise. Generate a comparison report with benchmark results first.";
      return;
    }

    const artifact = artifactSelect.value;
    const selectedArtifacts = artifacts.filter(([type]) => artifact === "all" || artifact === type);
    const summaries = artifact === "all" ? report.scanner_summaries ?? {} : report.artifact_summaries?.[artifact]?.scanners ?? {};
    const cases = artifact === "all" ? report.case_count : report.corpus_summary[artifact].case_count;
    const results = artifact === "all" ? report.scanner_case_result_count : (report.case_results ?? []).filter(row => row.artifact_type === artifact && row.applicable !== false).length;
    const supportedScanners = SCANNERS.filter(scanner => numeric(summaries[scanner]?.applicable_case_count) > 0).length;
    $("visualiseSummary").innerHTML = [
      [count(cases), "Benchmark cases", artifact === "all" ? "Across all artifact families" : artifactName(artifact)],
      [count(results), "Scanner-case results", "A case evaluated by one scanner"],
      [count(supportedScanners), "Scanners with results", "Applicable combinations only"],
    ].map(([value, label, description]) => `<article class="overview-card"><span>${label}</span><strong>${value}</strong><p>${escapeHtml(description)}</p></article>`).join("");

    $("visualiseScope").textContent = artifact === "all"
      ? "All artifacts · Scanner totals may cover different case sets. Select an artifact family for a like-for-like comparison. Unsupported cases are excluded from scores."
      : `${artifactName(artifact)} · All charts show this family only. Unsupported cases are excluded from scores.`;
    scannerCharts(report, artifact, summaries);
    detectionChart(report, artifact);
    familyChart(report, selectedArtifacts);
  }

  function loading() {
    $("visualise").setAttribute("aria-busy", "true");
    $("visualiseStatus").textContent = "Loading comparison report…";
    $("visualiseContent").hidden = true;
    $("visualiseEmpty").hidden = true;
    $("visualiseArtifact").disabled = true;
  }

  function error(message) {
    $("visualise").setAttribute("aria-busy", "false");
    $("visualiseContent").hidden = true;
    $("visualiseEmpty").hidden = false;
    $("visualiseArtifact").disabled = true;
    $("visualiseStatus").textContent = "Comparison report unavailable.";
    $("visualiseEmpty").innerHTML = `<h3>No chart data available</h3>
      <p>Open Comparison Report to generate a report, or use Refresh data to retry.</p>
      <p class="visualise-note">${escapeHtml(message)}</p>`;
  }

  return { render, loading, error };
})();
