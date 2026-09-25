/* =========================================================
   api.js
   Every network call to the backend lives here. Other files
   just call `API.predict()`, `API.scenario(...)` etc, so if
   an endpoint URL ever changes, you only edit this file.
========================================================= */

const API = {
  async _get(path) {
    const res = await fetch(`${BACKEND_URL}${path}`);
    if (!res.ok) {
      throw new Error(`Request failed (${res.status}): ${path}`);
    }
    return res.json();
  },

  async health() {
    return this._get("/api/health");
  },

  async predict(dataset = null) {
    const qs = dataset ? `?dataset=${encodeURIComponent(dataset)}` : "";
    return this._get(`/api/predict${qs}`);
  },

  async analysis(dataset = "customer_churn_cleaned.csv") {
    return this._get(`/api/analysis?dataset=${encodeURIComponent(dataset)}`);
  },

  async scenario({ growth = 6, elastic = 1.2, cost = 3.5, runs = 3000 } = {}) {
    const params = new URLSearchParams({ growth, elastic, cost, runs });
    return this._get(`/api/scenario?${params.toString()}`);
  },

  async knowledge(query) {
    return this._get(`/api/knowledge?q=${encodeURIComponent(query)}`);
  },

  async ask(query) {
    return this._get(`/api/ask?q=${encodeURIComponent(query)}`);
  },

  async datasets() {
    return this._get("/api/datasets");
  },

  async history() {
    return this._get("/api/history");
  },

  async upload(file) {
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${BACKEND_URL}/api/upload`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      throw new Error(`Upload failed (${res.status})`);
    }
    return res.json();
  },

  async realtime(datasetName, data) {
    const res = await fetch(`${BACKEND_URL}/api/realtime-data`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dataset_name: datasetName, data }),
    });
    if (!res.ok) {
      throw new Error(`Realtime ingest failed (${res.status})`);
    }
    return res.json();
  },
};
