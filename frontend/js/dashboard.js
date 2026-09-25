/* =========================================================
   dashboard.js
   Executive Overview page. Single call to /api/predict feeds
   every KPI tile, chart and the executive recommendation card
   on this page — all numbers are computed from the real CSVs.
========================================================= */

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function riskBadgeClass(risk) {
  if (risk === "Low") return "success";
  if (risk === "Medium") return "warning";
  return "danger";
}

async function loadDashboard() {
  const statusEl = document.getElementById("dashboardStatus");
  if (statusEl) statusEl.textContent = "Running Analysis, Forecasting, RAG and Decision agents…";

  try {
    const data = await API.predict();
    renderDashboard(data);
    if (statusEl) {
      statusEl.textContent = `Last run: ${new Date().toLocaleTimeString()} · live data from backend`;
    }
  } catch (err) {
    console.error(err);
    if (statusEl) {
      statusEl.textContent = `Unable to reach backend at ${BACKEND_URL}. Start the FastAPI server (see backend/README.md) then reload this page.`;
    }
  }
}

let dashboardRefreshTimer = null;

function startDashboardRefresh() {
  if (dashboardRefreshTimer) return;
  dashboardRefreshTimer = setInterval(() => loadDashboard(), 30000);
}

function renderDashboard(data) {
  // ---- KPI tiles -------------------------------------------------
  setText("kpiForecastAccuracy", `${data.forecast_accuracy}%`);
  setText("kpiGrowthRate", `${data.growth_rate}%`);
  setText("kpiChurnRate", `${data.churn_rate}%`);
  setText("kpiAttritionRate", `${data.attrition_rate}%`);

  const riskEl = document.getElementById("kpiRiskBadge");
  if (riskEl) {
    riskEl.textContent = data.decision.risk_level;
    riskEl.className = `badge ${riskBadgeClass(data.decision.risk_level)}`;
  }

  // ---- Revenue history + forecast chart ---------------------------
  const revLabels = [...data.revenue.labels, ...data.forecast.labels];
  const revActual = [...data.revenue.values, ...Array(data.forecast.values.length).fill(null)];
  const revForecast = [
    ...Array(data.revenue.values.length - 1).fill(null),
    data.revenue.values[data.revenue.values.length - 1],
    ...data.forecast.values,
  ];

  renderChart("revenueForecastChart", {
    type: "line",
    data: {
      labels: revLabels,
      datasets: [
        {
          label: "Actual revenue",
          data: revActual,
          borderColor: "#6AA2FF",
          backgroundColor: (ctx) => chartGradient(ctx.chart.ctx, "rgba(62,123,250,0.3)", "rgba(62,123,250,0)"),
          fill: true,
          tension: 0.35,
          pointRadius: 0,
          borderWidth: 2.5,
        },
        {
          label: "Forecast",
          data: revForecast,
          borderColor: "#22D3EE",
          borderDash: [6, 4],
          backgroundColor: "transparent",
          tension: 0.35,
          pointRadius: 0,
          borderWidth: 2.5,
        },
      ],
    },
    options: {
      responsive: true,
      aspectRatio: 2.6,
      plugins: { legend: { position: "bottom", labels: { boxWidth: 10, padding: 12 } } },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: CHART_DEFAULTS.gridColor } },
      },
    },
  });

  // ---- Churn by subscription tier ----------------------------------
  const churnLabels = Object.keys(data.churn_by_subscription);
  renderChart("churnBySubChart", {
    type: "bar",
    data: {
      labels: churnLabels,
      datasets: [
        {
          label: "Churn rate %",
          data: churnLabels.map((k) => data.churn_by_subscription[k]),
          backgroundColor: "#F8717188",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      aspectRatio: 1.7,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: CHART_DEFAULTS.gridColor } },
      },
    },
  });

  // ---- Attrition by city ---------------------------------------------
  const cityLabels = Object.keys(data.attrition_by_city);
  renderChart("attritionByCityChart", {
    type: "bar",
    data: {
      labels: cityLabels,
      datasets: [
        {
          label: "Attrition %",
          data: cityLabels.map((k) => data.attrition_by_city[k]),
          backgroundColor: "#3E7BFA88",
          borderRadius: 6,
        },
      ],
    },
    options: {
      responsive: true,
      aspectRatio: 1.7,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        y: { grid: { color: CHART_DEFAULTS.gridColor } },
      },
    },
  });

  // ---- Executive recommendation --------------------------------------
  const recList = document.getElementById("recommendationList");
  if (recList) {
    recList.innerHTML = data.decision.recommendation
      .map((r) => `<div class="insight-item">${r}</div>`)
      .join("");
  }

  // ---- Top retrieved knowledge passage --------------------------------
  const ragEl = document.getElementById("dashboardRagExcerpt");
  if (ragEl) {
    const top = (data.rag.results || [])[0];
    ragEl.innerHTML = top
      ? `${top.excerpt}<div class="chat-source">📄 ${top.doc_id}</div>`
      : "No knowledge base results.";
  }
}
