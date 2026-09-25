/* =========================================================
   scenario.js
   Scenario Simulator page — every slider change calls the
   real /api/scenario endpoint, which runs a Monte Carlo
   simulation server-side on top of the actual retail revenue
   total. Nothing here is computed client-side / faked.
========================================================= */

const SCENARIO_PRESETS = {
  bull: { growth: 16, elastic: 8, cost: 20, label: "Bull scenario" },
  base: { growth: 6, elastic: 12, cost: 35, label: "Base scenario" },
  bear: { growth: -4, elastic: 20, cost: 55, label: "Bear scenario" },
};

let scenarioDebounce = null;

function initScenario() {
  document.querySelectorAll(".btn[data-sc]").forEach((btn) =>
    btn.addEventListener("click", () => setScenarioPreset(btn.dataset.sc))
  );
  ["rangeGrowth", "rangeElastic", "rangeCost", "rangeRuns"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", () => runScenario());
  });
  const rerunBtn = document.getElementById("rerunScenarioBtn");
  if (rerunBtn) rerunBtn.addEventListener("click", () => runScenario());

  setScenarioPreset("base");
}

function setScenarioPreset(name) {
  document.querySelectorAll(".btn[data-sc]").forEach((btn) => btn.classList.remove("active"));
  const button = document.querySelector(`.btn[data-sc="${name}"]`);
  if (button) button.classList.add("active");

  const preset = SCENARIO_PRESETS[name];
  if (!preset) return;
  document.getElementById("rangeGrowth").value = preset.growth;
  document.getElementById("rangeElastic").value = preset.elastic;
  document.getElementById("rangeCost").value = preset.cost;
  setText("scenarioLabel", preset.label);
  runScenario();
}

function readSliderValues() {
  const growth = +document.getElementById("rangeGrowth").value;
  const elastic = +document.getElementById("rangeElastic").value / 10;
  const cost = +document.getElementById("rangeCost").value / 10;
  const runsIdx = +document.getElementById("rangeRuns").value;
  const runs = runsIdx * 1000;

  setText("valGrowth", `${growth}%`);
  setText("valElastic", `${elastic.toFixed(1)}x`);
  setText("valCost", `${cost.toFixed(1)}%`);
  setText("valRuns", runs.toLocaleString());

  return { growth, elastic, cost, runs };
}

async function runScenario() {
  const { growth, elastic, cost, runs } = readSliderValues();

  clearTimeout(scenarioDebounce);
  scenarioDebounce = setTimeout(async () => {
    const statusEl = document.getElementById("scenarioStatus");
    if (statusEl) statusEl.textContent = "Running Monte Carlo simulation on the backend…";
    try {
      const result = await API.scenario({ growth, elastic, cost, runs });
      renderScenario(result);
      if (statusEl) statusEl.textContent = "";
    } catch (err) {
      console.error(err);
      if (statusEl) statusEl.textContent = `Unable to reach backend at ${BACKEND_URL}.`;
    }
  }, 250);
}

function renderScenario(result) {
  setText("expRevenue", `$${result.expected_revenue}M`);
  setText("expRisk", `$${result.var_95}M`);
  setText("expSensitivity", result.sensitivity);

  renderChart("monteCarloChart", {
    type: "bar",
    data: {
      labels: result.histogram.labels,
      datasets: [
        {
          label: "Simulated outcomes",
          data: result.histogram.counts,
          backgroundColor: result.histogram.counts.map((_, i, arr) =>
            i < arr.length * 0.3 ? "#F8717188" : i > arr.length * 0.7 ? "#34D39988" : "#6AA2FF99"
          ),
          borderRadius: 4,
          barPercentage: 1,
          categoryPercentage: 1,
        },
      ],
    },
    options: {
      responsive: true,
      aspectRatio: 2.6,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { maxTicksLimit: 8 }, title: { display: true, text: "Revenue ($M)" } },
        y: { grid: { color: CHART_DEFAULTS.gridColor }, title: { display: true, text: "Frequency" } },
      },
    },
  });
}
