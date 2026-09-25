/* =========================================================
   charts.js
   Small shared helpers for building Chart.js charts, plus a
   registry so we can destroy/recreate charts cleanly when a
   view is refreshed (Chart.js throws if you draw on a canvas
   that already has a chart attached).
========================================================= */

const charts = {};

function chartGradient(ctx, colorTop, colorBottom, height = 240) {
  const gradient = ctx.createLinearGradient(0, 0, 0, height);
  gradient.addColorStop(0, colorTop);
  gradient.addColorStop(1, colorBottom);
  return gradient;
}

/** Destroy an existing chart on this canvas id (if any) then draw a new one. */
function renderChart(canvasId, config) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  if (charts[canvasId]) {
    charts[canvasId].destroy();
  }
  const ctx = canvas.getContext("2d");
  charts[canvasId] = new Chart(ctx, config);
  return charts[canvasId];
}

const CHART_DEFAULTS = {
  gridColor: "rgba(148,163,255,0.08)",
  textColor: "#9aa5c0",
};
