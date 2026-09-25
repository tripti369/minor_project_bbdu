/* =========================================================
   history.js
   Reports & History page — reads real rows back out of the
   SQLite database via GET /api/history, so this table always
   reflects genuine past runs, not placeholder data.
========================================================= */

async function loadReports() {
  const statusEl = document.getElementById("reportsStatus");
  if (statusEl) statusEl.textContent = "Loading history from the database…";

  try {
    const data = await API.history();
    renderReports(data);
    if (statusEl) statusEl.textContent = "";
  } catch (err) {
    console.error(err);
    if (statusEl) statusEl.textContent = `Unable to reach backend at ${BACKEND_URL}.`;
  }
}

function fmtDate(iso) {
  try {
    return new Date(iso + "Z").toLocaleString();
  } catch {
    return iso;
  }
}

function renderReports(data) {
  const predBody = document.getElementById("historyPredictionsBody");
  if (predBody) {
    predBody.innerHTML = data.predictions.length
      ? data.predictions
          .map(
            (p) => `<tr>
              <td>${fmtDate(p.created_at)}</td>
              <td>${p.forecast_accuracy}%</td>
              <td>${p.growth_rate}%</td>
              <td>${p.churn_rate}%</td>
              <td>${p.attrition_rate}%</td>
              <td><span class="badge ${riskBadgeClass(p.risk_level)}">${p.risk_level}</span></td>
            </tr>`
          )
          .join("")
      : `<tr><td colspan="6" class="loading-text">No prediction runs yet — visit the Dashboard to run one.</td></tr>`;
  }

  const scenBody = document.getElementById("historyScenariosBody");
  if (scenBody) {
    scenBody.innerHTML = data.scenarios.length
      ? data.scenarios
          .map(
            (s) => `<tr>
              <td>${fmtDate(s.created_at)}</td>
              <td>${s.growth}%</td>
              <td>${s.elastic}x</td>
              <td>${s.cost}%</td>
              <td>$${s.expected_revenue}M</td>
              <td>$${s.var_95}M</td>
            </tr>`
          )
          .join("")
      : `<tr><td colspan="6" class="loading-text">No scenario runs yet — visit the Scenario Simulator.</td></tr>`;
  }

  const uploadBody = document.getElementById("historyUploadsBody");
  if (uploadBody) {
    uploadBody.innerHTML = data.uploads.length
      ? data.uploads
          .map(
            (u) => `<tr>
              <td>${fmtDate(u.created_at)}</td>
              <td>${u.filename}</td>
              <td>${u.detected_type}</td>
              <td>${u.rows.toLocaleString()}</td>
              <td>${u.columns}</td>
              <td>${u.confidence}%</td>
            </tr>`
          )
          .join("")
      : `<tr><td colspan="6" class="loading-text">No uploads yet — visit the Data Upload page.</td></tr>`;
  }
}
