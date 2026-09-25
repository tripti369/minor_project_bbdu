/* =========================================================
   agents.js
   Describes the real Python agent modules that live in
   backend/app/agents/ — this is documentation of the actual
   architecture, not a simulation.
========================================================= */

const AGENTS = [
  {
    icon: "📊",
    name: "Analysis Agent",
    role: "backend/app/agents/analysis_agent.py",
    task: "Loads a dataset and computes basic statistics, descriptive statistics, a correlation matrix and an IQR-based outlier report.",
    endpoint: "GET /api/analysis",
  },
  {
    icon: "📈",
    name: "Forecasting Agent",
    role: "backend/app/agents/forecasting_agent.py",
    task: "Fits a Holt-Winters exponential smoothing model when there's enough seasonal history, otherwise falls back to a weighted moving average — and reports MAPE-based accuracy.",
    endpoint: "GET /api/predict",
  },
  {
    icon: "🎲",
    name: "Scenario Agent",
    role: "backend/app/agents/scenario_agent.py",
    task: "Runs a Monte Carlo simulation of revenue outcomes given growth, pricing elasticity and cost-inflation assumptions, seeded from the real retail revenue total.",
    endpoint: "GET /api/scenario",
  },
  {
    icon: "🔎",
    name: "RAG Agent",
    role: "backend/app/agents/rag_agent.py",
    task: "Indexes the local markdown knowledge base in persistent ChromaDB and returns the most relevant passages for a query with similarity scores.",
    endpoint: "GET /api/knowledge",
  },
  {
    icon: "🧭",
    name: "Decision Agent",
    role: "backend/app/agents/decision_agent.py",
    task: "Combines forecast accuracy, churn rate and attrition rate into a risk level (Low / Medium / High) and a short list of recommended actions.",
    endpoint: "Runs inside GET /api/predict",
  },
];

function renderAgents() {
  const grid = document.getElementById("agentCardsGrid");
  if (!grid) return;
  grid.innerHTML = AGENTS.map(
    (a) => `
    <div class="agent-card">
      <div class="agent-card-top">
        <div class="agent-avatar">${a.icon}</div>
        <div>
          <div class="agent-name">${a.name}</div>
          <div class="agent-role">${a.role}</div>
        </div>
      </div>
      <div class="agent-task">${a.task}</div>
      <div class="agent-endpoint">${a.endpoint}</div>
    </div>`
  ).join("");
}
