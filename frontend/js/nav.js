/* =========================================================
   nav.js
   Handles sidebar navigation: showing/hiding views and
   lazy-initializing each page's data the first time it's
   opened (so we don't call every endpoint on page load).
========================================================= */

const CRUMB_LABELS = {
  dashboard: "Dashboard",
  forecasting: "Forecasting",
  analytics: "Analytics",
  scenario: "Scenario Simulator",
  upload: "Data Upload",
  knowledge: "Knowledge Base",
  agents: "AI Agents",
  reports: "Reports & History",
};

const initializedViews = {};

function nav(viewName) {
  document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"));
  const target = document.getElementById("view-" + viewName);
  if (target) target.classList.add("active");

  document.querySelectorAll(".nav-item").forEach((n) => n.classList.remove("active"));
  const item = document.querySelector(`.nav-item[data-view="${viewName}"]`);
  if (item) item.classList.add("active");

  const crumb = document.getElementById("crumb-current");
  if (crumb) crumb.textContent = CRUMB_LABELS[viewName] || viewName;

  if (!initializedViews[viewName]) {
    initializedViews[viewName] = true;
    initView(viewName);
  }
}

function initView(viewName) {
  switch (viewName) {
    case "dashboard":
      loadDashboard();
      startDashboardRefresh();
      break;
    case "forecasting":
      loadForecasting();
      break;
    case "analytics":
      loadAnalytics();
      break;
    case "scenario":
      initScenario();
      break;
    case "upload":
      initUpload();
      break;
    case "knowledge":
      initKnowledge();
      break;
    case "agents":
      renderAgents();
      break;
    case "reports":
      loadReports();
      break;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".nav-item").forEach((item) =>
    item.addEventListener("click", () => nav(item.dataset.view))
  );
  nav("dashboard");
});
