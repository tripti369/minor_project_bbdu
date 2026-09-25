/* =========================================================
   forecasting.js
   Forecasting page — dataset selector drives the forecast
   chart and KPIs via /api/predict?dataset=...
========================================================= */

let _currentForecastDataset = null;

async function loadForecasting(dataset) {
  if (dataset !== undefined) _currentForecastDataset = dataset;

  const statusEl = document.getElementById("forecastingStatus");
  if (statusEl) statusEl.textContent = "Loading forecast…";

  try {
    const data = await API.predict(_currentForecastDataset);

    setText("fcAccuracy", `${data.forecast_accuracy}%`);
    setText("fcGrowth", `${data.growth_rate}%`);
    setText("fcMape", `${Math.max(0, (100 - data.forecast_accuracy)).toFixed(1)}%`);
    setText("fcHorizon", `${data.forecast.values.length} periods`);

    const labels = [...data.revenue.labels, ...data.forecast.labels];
    const actual = [...data.revenue.values, ...Array(data.forecast.values.length).fill(null)];
    const forecast = [
      ...Array(data.revenue.values.length - 1).fill(null),
      data.revenue.values[data.revenue.values.length - 1],
      ...data.forecast.values,
    ];

    renderChart("forecastDetailChart", {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Actual revenue",
            data: actual,
            borderColor: "#6AA2FF",
            backgroundColor: "transparent",
            borderWidth: 2.5,
            pointRadius: 3,
            tension: 0.35,
          },
          {
            label: "Forecast (next periods)",
            data: forecast,
            borderColor: "#22D3EE",
            borderDash: [6, 4],
            backgroundColor: "transparent",
            borderWidth: 2.5,
            pointRadius: 3,
            tension: 0.35,
          },
        ],
      },
      options: {
        responsive: true,
        aspectRatio: 2.4,
        plugins: { legend: { position: "bottom", labels: { boxWidth: 10, padding: 12 } } },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: CHART_DEFAULTS.gridColor }, title: { display: true, text: "Revenue" } },
        },
      },
    });

    const tableBody = document.getElementById("forecastTableBody");
    if (tableBody) {
      tableBody.innerHTML = data.forecast.labels
        .map(
          (label, i) =>
            `<tr><td>${label}</td><td>${data.forecast.values[i].toLocaleString()}</td></tr>`
        )
        .join("");
    }

    if (statusEl) statusEl.textContent = "";
  } catch (err) {
    console.error(err);
    if (statusEl) statusEl.textContent = `Unable to reach backend at ${BACKEND_URL}.`;
  }
}

async function initForecastingWithSelector() {
  const pageHead = document.querySelector("#view-forecasting .page-head");
  if (pageHead && !document.getElementById("forecastDatasetSelect")) {
    let datasets = [];
    try {
      const res = await API.datasets();
      datasets = (res.datasets || []).map(d => d.filename);
    } catch (_) {
      datasets = [
        "retail_warehouse_sales_cleaned.csv",
        "customer_churn_cleaned.csv",
        "employee_hr_cleaned.csv",
      ];
    }

    const sel = document.createElement("select");
    sel.id = "forecastDatasetSelect";
    sel.className = "select-input";
    sel.style.cssText = "width:auto;min-width:220px;";
    datasets.forEach(name => {
      const opt = document.createElement("option");
      opt.value = name;
      opt.textContent = name.replace(/_/g, " ").replace(".csv", "");
      if (name === "retail_warehouse_sales_cleaned.csv") opt.selected = true;
      sel.appendChild(opt);
    });
    sel.addEventListener("change", () => loadForecasting(sel.value));
    pageHead.appendChild(sel);
    _currentForecastDataset = sel.value;
  }

  loadForecasting();
}
