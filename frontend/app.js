"use strict";

/* ==========================================================================
   Scanner Benchmark Frontend
   Backend API version: 2.x
   ========================================================================== */

const SCANNERS = [
  "checkov",
  "trivy",
  "kubescape",
];

const VIEW_TITLES = {
  dashboard: "Dashboard",
  corpus: "Benchmark Corpus",
  run: "Process Benchmark",
  raw: "Raw Scanner Outputs",
  normalised: "Normalised Findings",
  matched: "Matching Results",
  metrics: "Per-Case Metrics",
  comparison: "Comparison Report",
  reports: "Reports",
  settings: "Settings",
};

const OUTPUT_STAGE_COPY = {
  raw: {
    title: "Raw scanner outputs",
    description:
      "Inspect the original machine-readable output produced by each scanner.",
  },

  normalised: {
    title: "Normalised findings",
    description:
      "Review scanner findings converted into the shared benchmark schema.",
  },

  matched: {
    title: "Matching results",
    description:
      "Review findings matched against the labelled ground truth.",
  },

  metrics: {
    title: "Metric output",
    description:
      "Inspect the generated precision, recall and F1 metric file.",
  },
};

const state = {
  view: "dashboard",

  cases: [],
  caseMap: new Map(),

  metrics: new Map(),

  latest: null,
  comparison: null,
  settings: null,
};


/* ==========================================================================
   DOM and formatting helpers
   ========================================================================== */

const $ = (id) => document.getElementById(id);


function on(id, eventName, handler) {
  const element = $(id);

  if (element) {
    element.addEventListener(
      eventName,
      handler,
    );
  }
}


function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}


function scannerName(scanner) {
  if (!scanner) {
    return "Unknown";
  }

  return (
    scanner.charAt(0).toUpperCase()
    + scanner.slice(1)
  );
}


function artifactName(artifactType) {
  const names = {
    kubernetes_yaml: "Kubernetes YAML",
    dockerfile: "Dockerfile",
    helm_chart: "Helm chart",
  };

  return names[artifactType] ?? artifactType ?? "Unknown";
}


function metric(value, decimalPlaces = 2) {
  const number = Number(value);

  if (!Number.isFinite(number)) {
    return "—";
  }

  return number.toFixed(decimalPlaces);
}


function integer(value) {
  const number = Number(value);

  if (!Number.isFinite(number)) {
    return "—";
  }

  return String(
    Math.trunc(number),
  );
}


function dateText(value) {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.valueOf())) {
    return "—";
  }

  return date.toLocaleString();
}


function joinValues(
  values,
  fallback = "—",
) {
  if (!Array.isArray(values)) {
    return fallback;
  }

  const filtered = values.filter(
    (value) => value !== null
      && value !== undefined
      && String(value).trim() !== "",
  );

  return filtered.length
    ? filtered.join(", ")
    : fallback;
}


function statusLabel(status) {
  const labels = {
    available: "Available",
    completed: "Completed",
    missing: "Not generated",
    failed: "Failed",
    invalid: "Invalid",
    not_applicable: "Not applicable",
    detected: "Detected",
    partial: "Partial",
    missed: "Missed",
    "no labelled result": "No labelled result",
  };

  const key = String(
    status ?? "",
  ).toLowerCase();

  return labels[key]
    ?? status
    ?? "Unknown";
}


function statusClass(status) {
  const key = String(
    status ?? "",
  ).toLowerCase();

  if (
    key === "available"
    || key === "completed"
    || key === "detected"
    || key === "valid"
  ) {
    return "success";
  }

  if (
    key === "failed"
    || key === "invalid"
    || key === "missed"
  ) {
    return "error";
  }

  if (
    key === "partial"
    || key === "warning"
  ) {
    return "warning";
  }

  return "neutral";
}


function pill(
  text,
  status = "neutral",
) {
  return `
    <span class="pill ${statusClass(status)}">
      ${escapeHtml(text)}
    </span>
  `;
}


function toast(
  message,
  type = "info",
) {
  const box = $("toast");

  if (!box) {
    return;
  }

  box.textContent = message;
  box.className = `toast ${type}`;
  box.hidden = false;

  clearTimeout(
    toast.timer,
  );

  toast.timer = setTimeout(
    () => {
      box.hidden = true;
    },
    4200,
  );
}


function errorMessage(error) {
  if (!error) {
    return "Unknown error.";
  }

  if (typeof error === "string") {
    return error;
  }

  if (error.message) {
    return error.message;
  }

  try {
    return JSON.stringify(
      error,
      null,
      2,
    );
  } catch {
    return String(error);
  }
}


/* ==========================================================================
   API helpers
   ========================================================================== */

function apiBase() {
  const saved = localStorage.getItem(
    "scannerBenchmarkApiBase",
  );

  if (saved !== null) {
    return saved.replace(
      /\/+$/,
      "",
    );
  }

  if (location.port === "8000") {
    return "";
  }

  return "http://127.0.0.1:8000";
}


function apiUrl(path) {
  return `${apiBase()}${path}`;
}


function extractApiError(data, status) {
  if (typeof data === "string") {
    return data || `HTTP ${status}`;
  }

  if (
    data
    && typeof data.detail === "string"
  ) {
    return data.detail;
  }

  if (
    data
    && data.detail
    && typeof data.detail === "object"
  ) {
    const detail = data.detail;

    if (
      detail.message
      && Array.isArray(detail.errors)
    ) {
      return [
        detail.message,
        ...detail.errors,
      ].join("\n");
    }

    if (detail.message) {
      return detail.message;
    }

    return JSON.stringify(
      detail,
      null,
      2,
    );
  }

  if (
    data
    && typeof data.message === "string"
  ) {
    return data.message;
  }

  try {
    return JSON.stringify(
      data,
      null,
      2,
    );
  } catch {
    return `HTTP ${status}`;
  }
}


async function request(
  path,
  options = {},
) {
  const controller = new AbortController();

  const timeout = setTimeout(
    () => controller.abort(),
    650000,
  );

  try {
    const response = await fetch(
      apiUrl(path),
      {
        ...options,

        headers: {
          "Content-Type": "application/json",
          ...(options.headers ?? {}),
        },

        signal: controller.signal,
      },
    );

    const contentType = (
      response.headers.get("content-type")
      ?? ""
    );

    let data;

    if (
      contentType.includes(
        "application/json",
      )
    ) {
      data = await response.json();
    } else {
      data = await response.text();
    }

    if (!response.ok) {
      throw new Error(
        extractApiError(
          data,
          response.status,
        ),
      );
    }

    return data;
  } catch (error) {
    if (
      error
      && error.name === "AbortError"
    ) {
      throw new Error(
        "The backend request timed out.",
      );
    }

    throw error;
  } finally {
    clearTimeout(timeout);
  }
}


/* ==========================================================================
   Backend health
   ========================================================================== */

function setConnection(
  online,
  text,
) {
  const connectionElement = $("connection");
  const sideDot = $("sideDot");
  const sideText = $("sideText");

  if (connectionElement) {
    connectionElement.className = (
      `connection ${
        online
          ? "online"
          : "offline"
      }`
    );

    const label = (
      connectionElement.querySelector("b")
    );

    if (label) {
      label.textContent = online
        ? "Backend connected"
        : "Backend offline";
    }
  }

  if (sideDot) {
    sideDot.className = online
      ? "online"
      : "offline";
  }

  if (sideText) {
    sideText.textContent = text;
  }
}


async function health(
  showToast = false,
) {
  try {
    const data = await request(
      "/api/health",
    );

    setConnection(
      true,
      `${
        data.project
        ?? "Scanner Benchmark API"
      } online`,
    );

    const versionElement = $(
      "apiVersion",
    );

    if (versionElement) {
      versionElement.textContent = (
        data.api_version
        ?? "—"
      );
    }

    if (showToast) {
      toast(
        "Backend connection successful.",
        "success",
      );
    }

    return true;
  } catch (error) {
    setConnection(
      false,
      errorMessage(error),
    );

    if (showToast) {
      toast(
        "Backend unavailable. Start Uvicorn on port 8000.",
        "error",
      );
    }

    return false;
  }
}


/* ==========================================================================
   Navigation
   ========================================================================== */

function showView(viewName) {
  state.view = viewName;

  document
    .querySelectorAll(".nav")
    .forEach((button) => {
      button.classList.toggle(
        "active",
        button.dataset.view === viewName,
      );
    });

  document
    .querySelectorAll(".view")
    .forEach((view) => {
      view.classList.remove(
        "active",
      );
    });

  let targetView = viewName;

  if (
    [
      "raw",
      "normalised",
      "matched",
    ].includes(viewName)
  ) {
    targetView = "output";

    setOutputStage(
      viewName,
    );
  }

  const view = $(targetView);

  if (!view) {
    toast(
      `The ${VIEW_TITLES[viewName] ?? viewName} view has not been added to index.html yet.`,
      "error",
    );

    return;
  }

  view.classList.add(
    "active",
  );

  const pageTitle = $("pageTitle");

  if (pageTitle) {
    pageTitle.textContent = (
      VIEW_TITLES[viewName]
      ?? "Scanner Benchmark"
    );
  }

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });

  if (viewName === "comparison") {
    loadComparison();
  }
}


/* ==========================================================================
   Cases and corpus
   ========================================================================== */

function getCase(caseId) {
  return state.caseMap.get(
    caseId,
  ) ?? null;
}


function selectCaseOptions(
  select,
  cases,
) {
  if (!select) {
    return;
  }

  const previousValue = select.value;

  select.innerHTML = cases
    .map((caseRecord) => {
      const label = (
        `${caseRecord.case_id} — `
        + `${caseRecord.artifact_label ?? artifactName(caseRecord.artifact_type)}`
      );

      return `
        <option value="${escapeHtml(caseRecord.case_id)}">
          ${escapeHtml(label)}
        </option>
      `;
    })
    .join("");

  const previousStillExists = (
    Array.from(select.options)
      .some(
        (option) => (
          option.value
          === previousValue
        ),
      )
  );

  if (previousStillExists) {
    select.value = previousValue;
  }
}


function fillCaseSelectors(cases) {
  const selectorIds = [
    "dashboardCase",
    "caseSelect",
    "outputCase",
    "metricsCase",
  ];

  selectorIds.forEach((id) => {
    selectCaseOptions(
      $(id),
      cases,
    );
  });

  updateScannerAvailability(
    $("caseSelect")?.value,
  );

  updateOutputScannerOptions(
    $("outputCase")?.value,
  );
}


function primaryMisconfiguration(
  caseRecord,
) {
  const subcategories = (
    caseRecord.subcategories
    ?? []
  );

  if (subcategories.length) {
    return subcategories.join(", ");
  }

  const categories = (
    caseRecord.categories
    ?? []
  );

  if (categories.length) {
    return categories.join(", ");
  }

  return "—";
}


function renderCorpusTable(cases) {
  const body = $("corpusTable");

  if (!body) {
    return;
  }

  if (!cases.length) {
    const columnCount = (
      body
        .closest("table")
        ?.querySelectorAll(
          "thead th",
        )
        .length
      ?? 6
    );

    body.innerHTML = `
      <tr>
        <td colspan="${columnCount}" class="empty">
          No configured benchmark cases were found.
        </td>
      </tr>
    `;

    return;
  }

  const headerCount = (
    body
      .closest("table")
      ?.querySelectorAll(
        "thead th",
      )
      .length
    ?? 6
  );

  body.innerHTML = cases
    .map((caseRecord) => {
      const validation = (
        caseRecord.validation_status
        ?? "unknown"
      );

      const severity = joinValues(
        caseRecord.severities,
      );

      const groundTruthIds = joinValues(
        caseRecord.ground_truth_ids,
      );

      const scanners = (
        caseRecord.applicable_scanners
        ?? []
      )
        .map(scannerName)
        .join(", ");

      /*
       * Existing six-column layout:
       * Case, artifact type, artifact, ground truth,
       * severity, validation.
       */
      if (headerCount <= 6) {
        return `
          <tr>
            <td>
              <strong>${escapeHtml(caseRecord.case_id)}</strong>
            </td>

            <td>
              ${escapeHtml(
                caseRecord.artifact_label
                ?? artifactName(caseRecord.artifact_type),
              )}
            </td>

            <td>
              ${escapeHtml(caseRecord.artifact_name ?? "—")}
            </td>

            <td>
              ${escapeHtml(groundTruthIds)}
            </td>

            <td>
              ${escapeHtml(severity)}
            </td>

            <td>
              ${pill(
                statusLabel(validation),
                validation,
              )}
            </td>
          </tr>
        `;
      }

      /*
       * New seven-column layout:
       * Case, artifact family, GT ID, misconfiguration,
       * severity, applicable scanners, validation.
       */
      return `
        <tr>
          <td>
            <strong>${escapeHtml(caseRecord.case_id)}</strong>
          </td>

          <td>
            ${escapeHtml(
              caseRecord.artifact_label
              ?? artifactName(caseRecord.artifact_type),
            )}
          </td>

          <td>
            ${escapeHtml(groundTruthIds)}
          </td>

          <td>
            ${escapeHtml(
              primaryMisconfiguration(caseRecord),
            )}
          </td>

          <td>
            ${escapeHtml(severity)}
          </td>

          <td>
            ${escapeHtml(scanners || "—")}
          </td>

          <td>
            ${pill(
              statusLabel(validation),
              validation,
            )}
          </td>
        </tr>
      `;
    })
    .join("");
}


function renderCorpusCounts(data) {
  const counts = (
    data.family_counts
    ?? {}
  );

  const values = {
    dashboardTotalCases:
      data.case_count,

    dashboardKubernetesCases:
      counts.kubernetes_yaml,

    dashboardDockerfileCases:
      counts.dockerfile,

    dashboardHelmCases:
      counts.helm_chart,
  };

  Object.entries(values)
    .forEach(
      ([id, value]) => {
        const element = $(id);

        if (element) {
          element.textContent = (
            integer(value)
          );
        }
      },
    );
}


async function loadCases() {
  const body = $("corpusTable");

  try {
    const data = await request(
      "/api/cases",
    );

    const cases = Array.isArray(
      data.cases,
    )
      ? data.cases
      : [];

    state.cases = cases;

    state.caseMap = new Map(
      cases.map(
        (caseRecord) => [
          caseRecord.case_id,
          caseRecord,
        ],
      ),
    );

    fillCaseSelectors(cases);
    renderCorpusTable(cases);
    renderCorpusCounts(data);

    return cases;
  } catch (error) {
    if (body) {
      const columnCount = (
        body
          .closest("table")
          ?.querySelectorAll(
            "thead th",
          )
          .length
        ?? 6
      );

      body.innerHTML = `
        <tr>
          <td colspan="${columnCount}" class="empty">
            Could not load the corpus:
            ${escapeHtml(errorMessage(error))}
          </td>
        </tr>
      `;
    }

    throw error;
  }
}


/* ==========================================================================
   Scanner applicability
   ========================================================================== */

function updateScannerAvailability(caseId) {
  const caseRecord = getCase(
    caseId,
  );

  const applicable = new Set(
    caseRecord?.applicable_scanners
    ?? SCANNERS,
  );

  document
    .querySelectorAll(
      'input[name="scanner"]',
    )
    .forEach((input) => {
      const isApplicable = applicable.has(
        input.value,
      );

      input.disabled = !isApplicable;

      if (!isApplicable) {
        input.checked = false;
      }

      const label = input.closest(
        ".scanner",
      );

      if (label) {
        label.classList.toggle(
          "disabled",
          !isApplicable,
        );

        label.setAttribute(
          "aria-disabled",
          String(!isApplicable),
        );

        let note = label.querySelector(
          ".applicability-note",
        );

        if (!isApplicable) {
          if (!note) {
            note = document.createElement(
              "small",
            );

            note.className = (
              "applicability-note"
            );

            label.appendChild(note);
          }

          note.textContent = (
            "Not applicable to this artifact type"
          );
        } else if (note) {
          note.remove();
        }
      }
    });
}


function updateOutputScannerOptions(caseId) {
  const select = $("outputScanner");

  if (!select) {
    return;
  }

  const caseRecord = getCase(
    caseId,
  );

  const applicable = new Set(
    caseRecord?.applicable_scanners
    ?? SCANNERS,
  );

  Array.from(select.options)
    .forEach((option) => {
      const isApplicable = applicable.has(
        option.value,
      );

      option.disabled = !isApplicable;

      option.textContent = (
        isApplicable
          ? scannerName(option.value)
          : `${scannerName(option.value)} — N/A`
      );
    });

  const selectedOption = (
    select.options[
      select.selectedIndex
    ]
  );

  if (
    !selectedOption
    || selectedOption.disabled
  ) {
    const firstApplicable = (
      Array.from(select.options)
        .find(
          (option) => !option.disabled,
        )
    );

    if (firstApplicable) {
      select.value = (
        firstApplicable.value
      );
    }
  }
}


/* ==========================================================================
   Per-case metrics
   ========================================================================== */

function standardMetricResult(
  result,
  caseId,
) {
  const counts = (
    result.counts
    ?? {}
  );

  const metrics = (
    result.metrics
    ?? {}
  );

  return {
    scanner:
      result.scanner,

    caseId:
      result.case_id
      ?? caseId,

    artifactType:
      result.artifact_type
      ?? getCase(caseId)?.artifact_type
      ?? null,

    applicable:
      result.applicable !== false,

    status:
      result.status
      ?? (
        result.metrics
          ? "available"
          : "missing"
      ),

    tp:
      Number(
        counts.true_positive_count
        ?? 0,
      ),

    fp:
      Number(
        counts.false_positive_count
        ?? 0,
      ),

    fn:
      Number(
        counts.false_negative_count
        ?? 0,
      ),

    extras:
      Number(
        counts.unlabelled_extra_findings_count
        ?? 0,
      ),

    duplicates:
      Number(
        counts.duplicate_match_count
        ?? 0,
      ),

    ambiguous:
      Number(
        counts.ambiguous_match_count
        ?? 0,
      ),

    precision:
      Number(metrics.precision),

    recall:
      Number(metrics.recall),

    f1:
      Number(
        metrics.f1_score
        ?? metrics.f1,
      ),

    matchingMode:
      result.matching_mode
      ?? null,

    updatedAt:
      result.updated_at
      ?? null,

    path:
      result.path
      ?? null,
  };
}


function metricCell(
  value,
  applicable,
) {
  if (!applicable) {
    return "N/A";
  }

  return metric(value);
}


function countCell(
  value,
  applicable,
) {
  if (!applicable) {
    return "N/A";
  }

  return integer(value);
}


function scannerStatusCell(row) {
  return pill(
    statusLabel(row.status),
    row.status,
  );
}


function renderMetrics(rows) {
  const dashboardTable = $(
    "dashboardTable",
  );

  const metricsTable = $(
    "metricsTable",
  );

  if (dashboardTable) {
    dashboardTable.innerHTML = rows
      .map((row) => `
        <tr
          class="${
            row.status === "available"
              ? "clickable"
              : ""
          }"
          data-case-id="${escapeHtml(row.caseId)}"
          data-scanner="${escapeHtml(row.scanner)}"
        >
          <td>
            <strong>${escapeHtml(scannerName(row.scanner))}</strong>
          </td>

          <td>
            ${scannerStatusCell(row)}
          </td>

          <td>${countCell(row.tp, row.applicable)}</td>
          <td>${countCell(row.fp, row.applicable)}</td>
          <td>${countCell(row.fn, row.applicable)}</td>
          <td>${countCell(row.extras, row.applicable)}</td>

          <td>${metricCell(row.precision, row.applicable)}</td>
          <td>${metricCell(row.recall, row.applicable)}</td>
          <td>${metricCell(row.f1, row.applicable)}</td>
        </tr>
      `)
      .join("");
  }

  if (metricsTable) {
    metricsTable.innerHTML = rows
      .map((row) => `
        <tr
          class="${
            row.status === "available"
              ? "clickable"
              : ""
          }"
          data-case-id="${escapeHtml(row.caseId)}"
          data-scanner="${escapeHtml(row.scanner)}"
        >
          <td>
            <strong>${escapeHtml(scannerName(row.scanner))}</strong>
            <br>
            ${scannerStatusCell(row)}
          </td>

          <td>${countCell(row.tp, row.applicable)}</td>
          <td>${countCell(row.fp, row.applicable)}</td>
          <td>${countCell(row.fn, row.applicable)}</td>
          <td>${countCell(row.extras, row.applicable)}</td>

          <td>${metricCell(row.precision, row.applicable)}</td>
          <td>${metricCell(row.recall, row.applicable)}</td>
          <td>${metricCell(row.f1, row.applicable)}</td>
        </tr>
      `)
      .join("");
  }

  document
    .querySelectorAll(
      "tr.clickable[data-scanner]",
    )
    .forEach((rowElement) => {
      rowElement.addEventListener(
        "click",
        () => {
          const key = (
            `${rowElement.dataset.caseId}:`
            + `${rowElement.dataset.scanner}`
          );

          const result = (
            state.metrics.get(key)
          );

          if (result) {
            selectMetric(result);
          }
        },
      );
    });
}


function clearMetricCards() {
  [
    "dashPrecision",
    "dashRecall",
    "dashF1",
    "metricPrecision",
    "metricRecall",
    "metricF1",
  ].forEach((id) => {
    const element = $(id);

    if (element) {
      element.textContent = "—";
    }
  });

  const precisionCounts = $(
    "precisionCounts",
  );

  if (precisionCounts) {
    precisionCounts.textContent = (
      "TP — · FP —"
    );
  }

  const recallCounts = $(
    "recallCounts",
  );

  if (recallCounts) {
    recallCounts.textContent = (
      "TP — · FN —"
    );
  }
}


function selectMetric(item) {
  const values = {
    dashPrecision:
      metric(item.precision),

    dashRecall:
      metric(item.recall),

    dashF1:
      metric(item.f1),

    metricPrecision:
      metric(item.precision),

    metricRecall:
      metric(item.recall),

    metricF1:
      metric(item.f1),
  };

  Object.entries(values)
    .forEach(
      ([id, value]) => {
        const element = $(id);

        if (element) {
          element.textContent = value;
        }
      },
    );

  const precisionCounts = $(
    "precisionCounts",
  );

  if (precisionCounts) {
    precisionCounts.textContent = (
      `TP ${item.tp} · FP ${item.fp}`
    );
  }

  const recallCounts = $(
    "recallCounts",
  );

  if (recallCounts) {
    recallCounts.textContent = (
      `TP ${item.tp} · FN ${item.fn}`
    );
  }

  setLatest({
    caseId: item.caseId,
    scanner: item.scanner,
    artifactType: item.artifactType,

    matchingMode:
      item.matchingMode
      ?? state.latest?.matchingMode
      ?? "review",

    status: "completed",

    updatedAt:
      item.updatedAt
      ?? new Date().toISOString(),
  });
}


function setLatest(latest) {
  state.latest = latest;

  const values = {
    latestCase:
      latest.caseId
      ?? "—",

    latestScanner:
      latest.scanner
        ? scannerName(latest.scanner)
        : "—",

    latestMode:
      latest.matchingMode
        ? latest.matchingMode.replace(
            /^./,
            (character) => (
              character.toUpperCase()
            ),
          )
        : "—",

    latestUpdated:
      dateText(latest.updatedAt),
  };

  Object.entries(values)
    .forEach(
      ([id, value]) => {
        const element = $(id);

        if (element) {
          element.textContent = value;
        }
      },
    );

  const artifactElement = $(
    "latestArtifact",
  );

  if (artifactElement) {
    artifactElement.textContent = (
      artifactName(
        latest.artifactType,
      )
    );
  }

  const statusElement = $(
    "latestStatus",
  );

  if (statusElement) {
    statusElement.className = (
      `pill ${statusClass(latest.status)}`
    );

    statusElement.textContent = (
      statusLabel(latest.status)
    );
  }
}


async function loadMetrics(caseId) {
  const resolvedCaseId = (
    caseId
    || $("metricsCase")?.value
    || $("dashboardCase")?.value
    || state.cases[0]?.case_id
  );

  if (!resolvedCaseId) {
    clearMetricCards();
    return [];
  }

  try {
    const response = await request(
      `/api/cases/${
        encodeURIComponent(resolvedCaseId)
      }/metrics`,
    );

    const rows = (
      response.results
      ?? []
    ).map(
      (result) => (
        standardMetricResult(
          result,
          resolvedCaseId,
        )
      ),
    );

    rows.forEach((row) => {
      state.metrics.set(
        `${row.caseId}:${row.scanner}`,
        row,
      );
    });

    renderMetrics(rows);

    const firstAvailable = rows.find(
      (row) => (
        row.status === "available"
      ),
    );

    if (firstAvailable) {
      selectMetric(firstAvailable);
    } else {
      clearMetricCards();
    }

    return rows;
  } catch (error) {
    clearMetricCards();

    const message = escapeHtml(
      errorMessage(error),
    );

    const dashboardTable = $(
      "dashboardTable",
    );

    const metricsTable = $(
      "metricsTable",
    );

    if (dashboardTable) {
      dashboardTable.innerHTML = `
        <tr>
          <td colspan="9" class="empty">
            Could not load metrics: ${message}
          </td>
        </tr>
      `;
    }

    if (metricsTable) {
      metricsTable.innerHTML = `
        <tr>
          <td colspan="8" class="empty">
            Could not load metrics: ${message}
          </td>
        </tr>
      `;
    }

    return [];
  }
}


/* ==========================================================================
   Benchmark processing
   ========================================================================== */

function consoleLog(message) {
  const box = $("console");

  if (!box) {
    return;
  }

  const timestamp = (
    new Date().toLocaleTimeString()
  );

  const entry = (
    `[${timestamp}] ${message}`
  );

  if (
    box.textContent.trim()
    === "Ready to run a benchmark."
  ) {
    box.textContent = entry;
  } else {
    box.textContent += (
      `\n${entry}`
    );
  }

  box.scrollTop = (
    box.scrollHeight
  );
}


function setProgress(value) {
  const bar = $("progressBar");

  if (bar) {
    bar.style.width = (
      `${value}%`
    );
  }
}


async function processBenchmark(event) {
  event.preventDefault();

  const caseId = (
    $("caseSelect")?.value
  );

  const matchingMode = (
    $("modeSelect")?.value
    ?? "review"
  );

  const selectedScanners = (
    Array.from(
      document.querySelectorAll(
        'input[name="scanner"]:checked:not(:disabled)',
      ),
    ).map(
      (input) => input.value,
    )
  );

  if (!caseId) {
    toast(
      "Select a benchmark case.",
      "error",
    );

    return;
  }

  if (!selectedScanners.length) {
    toast(
      "Select at least one applicable scanner.",
      "error",
    );

    return;
  }

  const runButton = $("runBtn");

  if (runButton) {
    runButton.disabled = true;
    runButton.textContent = (
      "Processing benchmark…"
    );
  }

  setProgress(10);

  consoleLog(
    `Starting ${matchingMode} processing for ${caseId}.`,
  );

  consoleLog(
    `Selected scanners: ${selectedScanners.join(", ")}.`,
  );

  try {
    const response = await request(
      "/api/process",
      {
        method: "POST",

        body: JSON.stringify({
          case_id: caseId,
          scanners: selectedScanners,
          matching_mode: matchingMode,
        }),
      },
    );

    setProgress(85);

    const results = (
      response.results
      ?? []
    );

    results.forEach((result) => {
      consoleLog(
        `${scannerName(result.scanner)}: ${statusLabel(result.status)}.`,
      );

      if (
        Array.isArray(result.command)
        && result.command.length
      ) {
        consoleLog(
          `Command: ${result.command.join(" ")}`,
        );
      }

      if (
        result.console_output
        && result.console_output.trim()
      ) {
        consoleLog(
          result.console_output.trim(),
        );
      }

      if (result.error) {
        consoleLog(
          `Error: ${errorMessage(result.error)}`,
        );
      }
    });

    setProgress(100);

    if (
      Number(response.completed_count)
      > 0
    ) {
      const completed = results.filter(
        (result) => (
          result.status === "completed"
        ),
      );

      const latestResult = (
        completed.at(-1)
      );

      setLatest({
        caseId,
        scanner:
          latestResult?.scanner
          ?? null,

        artifactType:
          response.artifact_type,

        matchingMode,

        status:
          response.failed_count
            ? "partial"
            : "completed",

        updatedAt:
          response.completed_at
          ?? new Date().toISOString(),
      });

      toast(
        `${response.completed_count} scanner pipeline(s) completed.`,
        response.failed_count
          ? "warning"
          : "success",
      );
    } else {
      toast(
        "No scanner pipeline completed. Review the execution console.",
        "error",
      );
    }

    await Promise.all([
      loadMetrics(caseId),
      loadReports(),
    ]);
  } catch (error) {
    consoleLog(
      `Benchmark processing failed: ${errorMessage(error)}`,
    );

    toast(
      `Benchmark processing failed: ${errorMessage(error)}`,
      "error",
    );
  } finally {
    if (runButton) {
      runButton.disabled = false;
      runButton.textContent = (
        "Process selected scanners"
      );
    }

    setTimeout(
      () => setProgress(0),
      1000,
    );
  }
}


async function loadSavedResults() {
  const caseId = (
    $("caseSelect")?.value
  );

  const rows = await loadMetrics(
    caseId,
  );

  const availableCount = rows.filter(
    (row) => (
      row.status === "available"
    ),
  ).length;

  if (availableCount) {
    toast(
      `${availableCount} saved metric file(s) loaded.`,
      "success",
    );

    showView("metrics");
  } else {
    toast(
      "No saved metric files were found for this case.",
      "error",
    );
  }
}


/* ==========================================================================
   Raw, normalised, matched and metrics output
   ========================================================================== */

function setOutputStage(stage) {
  const select = $("outputStage");

  if (select) {
    select.value = stage;
  }

  const copy = (
    OUTPUT_STAGE_COPY[stage]
    ?? OUTPUT_STAGE_COPY.raw
  );

  const title = $("outputTitle");
  const description = $("outputDesc");

  if (title) {
    title.textContent = copy.title;
  }

  if (description) {
    description.textContent = (
      copy.description
    );
  }
}


async function loadOutput() {
  const stage = (
    $("outputStage")?.value
    ?? "raw"
  );

  const scanner = (
    $("outputScanner")?.value
  );

  const caseId = (
    $("outputCase")?.value
  );

  const viewer = $("outputViewer");

  if (!viewer) {
    return;
  }

  if (
    !scanner
    || !caseId
  ) {
    viewer.textContent = (
      "Select a case and scanner."
    );

    return;
  }

  const caseRecord = getCase(
    caseId,
  );

  if (
    caseRecord
    && !caseRecord.applicable_scanners.includes(
      scanner,
    )
  ) {
    viewer.textContent = (
      `${scannerName(scanner)} is not applicable `
      + `to ${caseRecord.artifact_label}.`
    );

    return;
  }

  viewer.textContent = (
    "Loading output…"
  );

  try {
    const data = await request(
      `/api/outputs/${
        encodeURIComponent(stage)
      }/${
        encodeURIComponent(scanner)
      }?case_id=${
        encodeURIComponent(caseId)
      }`,
    );

    const header = [
      `Case: ${data.case_id}`,
      `Artifact: ${data.artifact_label}`,
      `Scanner: ${scannerName(data.scanner)}`,
      `Stage: ${data.stage}`,
      `Path: ${data.path}`,
      `Updated: ${dateText(data.updated_at)}`,
      "",
    ].join("\n");

    viewer.textContent = (
      header
      + JSON.stringify(
        data.data,
        null,
        2,
      )
    );
  } catch (error) {
    viewer.textContent = (
      "Could not load output.\n\n"
      + errorMessage(error)
    );
  }
}


/* ==========================================================================
   Combined comparison report
   ========================================================================== */

function setTextIfPresent(
  id,
  value,
) {
  const element = $(id);

  if (element) {
    element.textContent = value;
  }
}


function renderOverallScannerSummary(
  report,
) {
  const body = $(
    "overallScannerTable",
  );

  if (!body) {
    return;
  }

  const summaries = (
    report.scanner_summaries
    ?? {}
  );

  body.innerHTML = SCANNERS
    .map((scanner) => {
      const summary = (
        summaries[scanner]
        ?? {}
      );

      return `
        <tr>
          <td>
            <strong>${escapeHtml(scannerName(scanner))}</strong>
          </td>

          <td>${integer(summary.applicable_case_count)}</td>
          <td>${integer(summary.not_applicable_case_count)}</td>
          <td>${integer(summary.true_positive_count)}</td>
          <td>${integer(summary.false_positive_count)}</td>
          <td>${integer(summary.false_negative_count)}</td>
          <td>${integer(summary.unlabelled_extra_findings_count)}</td>

          <td>${metric(summary.micro_precision, 4)}</td>
          <td>${metric(summary.micro_recall, 4)}</td>
          <td>${metric(summary.micro_f1_score, 4)}</td>
          <td>${metric(summary.macro_f1_score, 4)}</td>
        </tr>
      `;
    })
    .join("");
}


function renderCoverageMatrix(
  report,
) {
  const body = $(
    "comparisonCoverageTable",
  );

  if (!body) {
    return;
  }

  const rows = (
    report.coverage_matrix
    ?? []
  );

  if (!rows.length) {
    body.innerHTML = `
      <tr>
        <td colspan="5" class="empty">
          No coverage information is available.
        </td>
      </tr>
    `;

    return;
  }

  body.innerHTML = rows
    .map((row) => {
      const scannerResults = (
        row.scanners
        ?? {}
      );

      return `
        <tr>
          <td>
            <strong>${escapeHtml(row.case_id)}</strong>
          </td>

          <td>
            ${escapeHtml(
              row.artifact_label
              ?? artifactName(row.artifact_type),
            )}
          </td>

          <td>
            ${pill(
              scannerResults.checkov
              ?? "Unknown",

              scannerResults.checkov
              ?? "neutral",
            )}
          </td>

          <td>
            ${pill(
              scannerResults.trivy
              ?? "Unknown",

              scannerResults.trivy
              ?? "neutral",
            )}
          </td>

          <td>
            ${pill(
              scannerResults.kubescape
              ?? "Unknown",

              scannerResults.kubescape
              ?? "neutral",
            )}
          </td>
        </tr>
      `;
    })
    .join("");
}


function renderArtifactSummary(
  report,
) {
  const body = $(
    "comparisonArtifactTable",
  );

  if (!body) {
    return;
  }

  const summaries = (
    report.artifact_summaries
    ?? {}
  );

  const rows = [];

  [
    "kubernetes_yaml",
    "dockerfile",
    "helm_chart",
  ].forEach((artifactType) => {
    const artifactSummary = (
      summaries[artifactType]
    );

    if (!artifactSummary) {
      return;
    }

    Object.entries(
      artifactSummary.scanners
      ?? {},
    ).forEach(
      ([scanner, summary]) => {
        rows.push(`
          <tr>
            <td>
              ${escapeHtml(
                artifactSummary.label
                ?? artifactName(artifactType),
              )}
            </td>

            <td>
              <strong>${escapeHtml(scannerName(scanner))}</strong>
            </td>

            <td>${integer(summary.applicable_case_count)}</td>
            <td>${integer(summary.true_positive_count)}</td>
            <td>${integer(summary.false_positive_count)}</td>
            <td>${integer(summary.false_negative_count)}</td>
            <td>${integer(summary.unlabelled_extra_findings_count)}</td>

            <td>${metric(summary.micro_precision, 4)}</td>
            <td>${metric(summary.micro_recall, 4)}</td>
            <td>${metric(summary.micro_f1_score, 4)}</td>
            <td>${metric(summary.macro_f1_score, 4)}</td>
          </tr>
        `);
      },
    );
  });

  body.innerHTML = rows.length
    ? rows.join("")
    : `
      <tr>
        <td colspan="11" class="empty">
          No artifact summary is available.
        </td>
      </tr>
    `;
}


function renderComparisonCases(
  report,
) {
  const body = $(
    "comparisonCaseTable",
  );

  if (!body) {
    return;
  }

  const rows = (
    report.case_results
    ?? []
  );

  if (!rows.length) {
    body.innerHTML = `
      <tr>
        <td colspan="10" class="empty">
          No per-case comparison results are available.
        </td>
      </tr>
    `;

    return;
  }

  body.innerHTML = rows
    .map((row) => `
      <tr>
        <td>
          <strong>${escapeHtml(row.case_id)}</strong>
        </td>

        <td>
          ${escapeHtml(
            row.artifact_label
            ?? artifactName(row.artifact_type),
          )}
        </td>

        <td>
          ${escapeHtml(scannerName(row.scanner))}
        </td>

        <td>${integer(row.true_positive_count)}</td>
        <td>${integer(row.false_positive_count)}</td>
        <td>${integer(row.false_negative_count)}</td>

        <td>
          ${integer(row.unlabelled_extra_findings_count)}
        </td>

        <td>${metric(row.precision, 4)}</td>
        <td>${metric(row.recall, 4)}</td>
        <td>${metric(row.f1_score, 4)}</td>
      </tr>
    `)
    .join("");
}


function renderComparison(report) {
  state.comparison = report;

  setTextIfPresent(
    "comparisonUpdated",
    dateText(
      report.updated_at
      ?? report.generated_at_utc,
    ),
  );

  setTextIfPresent(
    "dashboardTotalCases",
    integer(report.case_count),
  );

  setTextIfPresent(
    "dashboardScannerRuns",
    integer(
      report.scanner_case_result_count,
    ),
  );

  const corpus = (
    report.corpus_summary
    ?? {}
  );

  setTextIfPresent(
    "dashboardKubernetesCases",
    integer(
      corpus.kubernetes_yaml?.case_count,
    ),
  );

  setTextIfPresent(
    "dashboardDockerfileCases",
    integer(
      corpus.dockerfile?.case_count,
    ),
  );

  setTextIfPresent(
    "dashboardHelmCases",
    integer(
      corpus.helm_chart?.case_count,
    ),
  );

  renderOverallScannerSummary(report);
  renderCoverageMatrix(report);
  renderArtifactSummary(report);
  renderComparisonCases(report);
}


async function loadComparison(
  showToast = false,
) {
  const status = $(
    "comparisonStatus",
  );

  if (status) {
    status.textContent = (
      "Loading comparison report…"
    );
  }

  try {
    const report = await request(
      "/api/comparison",
    );

    renderComparison(report);

    if (status) {
      status.textContent = (
        `Loaded ${report.case_count ?? 0} cases `
        + `and ${report.scanner_case_result_count ?? 0} scanner-case results.`
      );
    }

    if (showToast) {
      toast(
        "Comparison report loaded.",
        "success",
      );
    }

    if ($("comparisonMarkdown")) {
      await loadComparisonMarkdown();
    }

    return report;
  } catch (error) {
    if (status) {
      status.textContent = (
        "The comparison report has not been generated."
      );
    }

    if (showToast) {
      toast(
        `Could not load comparison report: ${errorMessage(error)}`,
        "error",
      );
    }

    return null;
  }
}


async function loadComparisonMarkdown() {
  const viewer = $(
    "comparisonMarkdown",
  );

  if (!viewer) {
    return;
  }

  viewer.textContent = (
    "Loading comparison report…"
  );

  try {
    const response = await fetch(
      apiUrl(
        "/api/comparison/markdown",
      ),
    );

    if (!response.ok) {
      const text = await response.text();

      throw new Error(
        text || `HTTP ${response.status}`,
      );
    }

    viewer.textContent = (
      await response.text()
    );
  } catch (error) {
    viewer.textContent = (
      "Could not load comparison Markdown.\n\n"
      + errorMessage(error)
    );
  }
}


async function generateComparison() {
  const button = $(
    "generateComparisonBtn",
  );

  if (button) {
    button.disabled = true;
    button.textContent = (
      "Generating comparison…"
    );
  }

  try {
    const response = await request(
      "/api/comparison/generate",
      {
        method: "POST",
      },
    );

    if (
      response.console_output
      && $("comparisonConsole")
    ) {
      $("comparisonConsole").textContent = (
        response.console_output
      );
    }

    toast(
      "Comparison report generated successfully.",
      "success",
    );

    await loadComparison();
  } catch (error) {
    toast(
      `Comparison generation failed: ${errorMessage(error)}`,
      "error",
    );
  } finally {
    if (button) {
      button.disabled = false;
      button.textContent = (
        "Generate comparison"
      );
    }
  }
}


/* ==========================================================================
   Reports
   ========================================================================== */

async function loadReports() {
  const reportList = $(
    "reportList",
  );

  if (!reportList) {
    return [];
  }

  try {
    const data = await request(
      "/api/reports",
    );

    const reports = Array.isArray(
      data.reports,
    )
      ? data.reports
      : [];

    if (!reports.length) {
      reportList.innerHTML = `
        <p class="empty">
          No generated Markdown reports were found.
        </p>
      `;

      return [];
    }

    reportList.innerHTML = reports
      .map((report) => `
        <button
          class="report-item"
          data-report-id="${escapeHtml(report.id)}"
          data-report-name="${escapeHtml(report.name)}"
        >
          <strong>
            ${escapeHtml(report.name)}
          </strong>

          <small>
            ${escapeHtml(report.artifact_label ?? report.report_group)}
            · ${escapeHtml(dateText(report.modified_at))}
          </small>
        </button>
      `)
      .join("");

    document
      .querySelectorAll(
        ".report-item",
      )
      .forEach((button) => {
        button.addEventListener(
          "click",
          () => {
            openReport(
              button.dataset.reportId,
              button.dataset.reportName,
              button,
            );
          },
        );
      });

    return reports;
  } catch (error) {
    reportList.innerHTML = `
      <p class="empty">
        Could not load reports:
        ${escapeHtml(errorMessage(error))}
      </p>
    `;

    return [];
  }
}


async function openReport(
  reportId,
  reportName,
  button,
) {
  document
    .querySelectorAll(
      ".report-item",
    )
    .forEach((item) => {
      item.classList.remove(
        "active",
      );
    });

  if (button) {
    button.classList.add(
      "active",
    );
  }

  const title = $("reportTitle");
  const viewer = $("reportViewer");

  if (title) {
    title.textContent = (
      reportName
      ?? "Report preview"
    );
  }

  if (!viewer) {
    return;
  }

  viewer.textContent = (
    "Loading report…"
  );

  try {
    const response = await fetch(
      apiUrl(
        `/api/reports/${
          encodeURIComponent(reportId)
        }`,
      ),
    );

    if (!response.ok) {
      const text = await response.text();

      throw new Error(
        text || `HTTP ${response.status}`,
      );
    }

    viewer.textContent = (
      await response.text()
    );
  } catch (error) {
    viewer.textContent = (
      "Could not load report.\n\n"
      + errorMessage(error)
    );
  }
}


/* ==========================================================================
   Settings
   ========================================================================== */

async function loadSettings() {
  try {
    const settings = await request(
      "/api/settings",
    );

    state.settings = settings;

    setTextIfPresent(
      "settingsProjectRoot",
      settings.project_root
      ?? "—",
    );

    setTextIfPresent(
      "settingsConfigPath",
      settings.configuration
      ?? "—",
    );

    setTextIfPresent(
      "settingsRawRoot",
      settings.raw_root
      ?? "—",
    );

    setTextIfPresent(
      "settingsComparisonRoot",
      settings.comparison_root
      ?? "—",
    );

    document
      .querySelectorAll(
        "[data-setting-path]",
      )
      .forEach((element) => {
        const key = (
          element.dataset.settingPath
        );

        const value = key
          .split(".")
          .reduce(
            (
              current,
              part,
            ) => current?.[part],
            settings,
          );

        if (
          value !== undefined
          && value !== null
        ) {
          element.textContent = (
            Array.isArray(value)
              ? value.join(", ")
              : String(value)
          );
        }
      });

    return settings;
  } catch {
    return null;
  }
}


function saveApiSettings() {
  const input = $("apiInput");

  if (!input) {
    return;
  }

  const value = (
    input.value
      .trim()
      .replace(
        /\/+$/,
        "",
      )
  );

  localStorage.setItem(
    "scannerBenchmarkApiBase",
    value,
  );

  toast(
    "API setting saved.",
    "success",
  );

  health(true);
}


/* ==========================================================================
   Refresh controls
   ========================================================================== */

async function refresh() {
  const online = await health();

  if (!online) {
    toast(
      "Backend unavailable. Start FastAPI first.",
      "error",
    );

    return;
  }

  try {
    if (state.view === "corpus") {
      await loadCases();
    } else if (
      state.view === "reports"
    ) {
      await loadReports();
    } else if (
      state.view === "comparison"
    ) {
      await loadComparison();
    } else if (
      state.view === "metrics"
    ) {
      await loadMetrics(
        $("metricsCase")?.value,
      );
    } else if (
      state.view === "dashboard"
    ) {
      await Promise.all([
        loadMetrics(
          $("dashboardCase")?.value,
        ),
        loadComparison(),
      ]);
    } else if (
      [
        "raw",
        "normalised",
        "matched",
      ].includes(state.view)
    ) {
      await loadOutput();
    } else {
      await Promise.all([
        loadCases(),
        loadReports(),
        loadComparison(),
        loadSettings(),
      ]);
    }

    toast(
      "Data refreshed.",
      "success",
    );
  } catch (error) {
    toast(
      `Refresh failed: ${errorMessage(error)}`,
      "error",
    );
  }
}


/* ==========================================================================
   Event binding
   ========================================================================== */

function bindNavigation() {
  document
    .querySelectorAll(".nav")
    .forEach((button) => {
      button.addEventListener(
        "click",
        () => {
          showView(
            button.dataset.view,
          );
        },
      );
    });

  document
    .querySelectorAll(".goto")
    .forEach((button) => {
      button.addEventListener(
        "click",
        () => {
          showView(
            button.dataset.target,
          );
        },
      );
    });
}


function bindCaseSelectors() {
  on(
    "caseSelect",
    "change",
    () => {
      updateScannerAvailability(
        $("caseSelect").value,
      );
    },
  );

  on(
    "dashboardCase",
    "change",
    () => {
      loadMetrics(
        $("dashboardCase").value,
      );
    },
  );

  on(
    "metricsCase",
    "change",
    () => {
      loadMetrics(
        $("metricsCase").value,
      );
    },
  );

  on(
    "outputCase",
    "change",
    () => {
      updateOutputScannerOptions(
        $("outputCase").value,
      );
    },
  );
}


function bindControls() {
  on(
    "refreshBtn",
    "click",
    refresh,
  );

  on(
    "reloadCases",
    "click",
    loadCases,
  );

  on(
    "runForm",
    "submit",
    processBenchmark,
  );

  on(
    "loadSavedBtn",
    "click",
    loadSavedResults,
  );

  on(
    "clearConsole",
    "click",
    () => {
      const consoleElement = $(
        "console",
      );

      if (consoleElement) {
        consoleElement.textContent = (
          "Ready to run a benchmark."
        );
      }
    },
  );

  on(
    "loadOutputBtn",
    "click",
    loadOutput,
  );

  on(
    "outputStage",
    "change",
    () => {
      setOutputStage(
        $("outputStage").value,
      );
    },
  );

  on(
    "reloadMetrics",
    "click",
    () => {
      loadMetrics(
        $("metricsCase")?.value,
      );
    },
  );

  on(
    "reloadReports",
    "click",
    loadReports,
  );

  on(
    "reloadComparison",
    "click",
    () => {
      loadComparison(true);
    },
  );

  on(
    "generateComparisonBtn",
    "click",
    generateComparison,
  );

  on(
    "saveApi",
    "click",
    saveApiSettings,
  );

  on(
    "testApi",
    "click",
    () => health(true),
  );
}


function bind() {
  bindNavigation();
  bindCaseSelectors();
  bindControls();
}


/* ==========================================================================
   Application startup
   ========================================================================== */

async function initialise() {
  bind();

  const apiInput = $("apiInput");

  if (apiInput) {
    apiInput.value = (
      apiBase()
      || location.origin
    );
  }

  const online = await health();

  if (!online) {
    toast(
      "Frontend loaded, but the backend is not reachable. Start Uvicorn on port 8000.",
      "error",
    );

    return;
  }

  try {
    await loadCases();

    const initialCaseId = (
      $("dashboardCase")?.value
      ?? state.cases[0]?.case_id
    );

    await Promise.all([
      initialCaseId
        ? loadMetrics(initialCaseId)
        : Promise.resolve([]),

      loadReports(),
      loadComparison(),
      loadSettings(),
    ]);
  } catch (error) {
    toast(
      `Initial data loading failed: ${errorMessage(error)}`,
      "error",
    );
  }
}


document.addEventListener(
  "DOMContentLoaded",
  initialise,
);