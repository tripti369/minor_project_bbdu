/* =========================================================
   analytics.js
   Analytics page — dataset selector drives all charts/stats
   via the Analysis Agent on the real CSV datasets.
========================================================= */

let _currentAnalyticsDataset = "customer_churn_cleaned.csv";

async function loadAnalytics(dataset) {
  if (dataset) _currentAnalyticsDataset = dataset;

  const statusEl = document.getElementById("analyticsStatus");
  if (statusEl) statusEl.textContent = "Running Analysis Agent…";

  try {
    const data = await API.analysis(_currentAnalyticsDataset);
    renderAnalytics(data);
    if (statusEl) statusEl.textContent = "";
  } catch (err) {
    console.error(err);
    if (statusEl) statusEl.textContent = `Unable to reach backend at ${BACKEND_URL}.`;
  }
}

async function initAnalyticsWithSelector() {
  // Build dataset selector if not already present
  const pageHead = document.querySelector("#view-analytics .page-head");
  if (pageHead && !document.getElementById("analyticsDatasetSelect")) {
    let datasets = [];
    try {
      const res = await API.datasets();
      datasets = (res.datasets || []).map(d => d.filename);
    } catch (_) {
      datasets = [
        "customer_churn_cleaned.csv",
        "employee_hr_cleaned.csv",
        "retail_warehouse_sales_cleaned.csv",
      ];
    }

    const sel = document.createElement("select");
    sel.id = "analyticsDatasetSelect";
    sel.className = "select-input";
    sel.style.cssText = "width:auto;min-width:220px;";
    datasets.forEach(name => {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name.replace(/_/g, " ").replace(".csv", "");
      if (name === _currentAnalyticsDataset) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener("change", () => loadAnalytics(sel.value));
    pageHead.appendChild(sel);
  }

  loadAnalytics(_currentAnalyticsDataset);
}

function renderAnalytics(data) {
  setText("statRows", data.basic_statistics.rows.toLocaleString());
  setText("statColumns", data.basic_statistics.columns);
  setText("statDuplicates", data.basic_statistics.duplicate_rows);
  const totalMissing = Object.values(data.basic_statistics.missing_values || {}).reduce((a, b) => a + b, 0);
  setText("statMissing", totalMissing);

  // ---- Correlation heatmap -----------------------------------------
  const corr = data.correlation || {};
  const vars = Object.keys(corr);
  const corrGrid = document.getElementById("corrMatrix");
  if (corrGrid) {
    corrGrid.style.gridTemplateColumns = `repeat(${vars.length || 1}, 1fr)`;
    let html = "";
    vars.forEach((rowVar) => {
      vars.forEach((colVar) => {
        const v = corr[rowVar][colVar];
        const intensity = Math.abs(v);
        const color =
          v >= 0
            ? `rgba(34,211,238,${0.15 + intensity * 0.6})`
            : `rgba(248,113,113,${0.15 + intensity * 0.6})`;
        html += `<div class="heat-cell" title="${rowVar} vs ${colVar}" style="background:${color};">${v.toFixed(2)}</div>`;
      });
    });
    corrGrid.innerHTML = html;
  }
  const corrLegend = document.getElementById("corrLegend");
  if (corrLegend) corrLegend.textContent = vars.join(" · ");

  // ---- Outlier chart --------------------------------------------------
  const outlierCols = Object.keys(data.outlier_report || {});
  renderChart("outlierChart", {
    type: "bar",
    data: {
      labels: outlierCols,
      datasets: [
        {
          label: "Outlier %",
          data: outlierCols.map((c) => data.outlier_report[c].outlier_percentage),
          backgroundColor: "#F8717199",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      aspectRatio: 2.4,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { autoSkip: false, maxRotation: 45, minRotation: 0 } },
        y: { grid: { color: CHART_DEFAULTS.gridColor }, title: { display: true, text: "% of rows" } },
      },
    },
  });

  // ---- Descriptive stats table ------------------------------------------
  const desc = data.descriptive_statistics || {};
  const cols = Object.keys(desc);
  const statRows = ["mean", "std", "min", "50%", "max"];
  const tbody = document.getElementById("descStatsBody");
  if (tbody) {
    tbody.innerHTML = statRows
      .map((stat) => {
        const cells = cols.map((c) => `<td>${desc[c][stat] !== undefined ? desc[c][stat] : "—"}</td>`).join("");
        return `<tr><td><b>${stat}</b></td>${cells}</tr>`;
      })
      .join("");
  }
  const thead = document.getElementById("descStatsHead");
  if (thead) {
    thead.innerHTML = `<th></th>${cols.map((c) => `<th>${c}</th>`).join("")}`;
  }
}
