# Frontend — Predictive Intelligence Engine

Plain HTML/CSS/JS. No framework, no build step, no npm install needed.

## Run

Easiest way — just open the file:

```
Double-click frontend/index.html
```

Recommended way (avoids browser file:// restrictions):

```bash
cd frontend
python -m http.server 5500
```

Then open `http://127.0.0.1:5500` in your browser.

Make sure the **backend** is running first at `http://127.0.0.1:8000`
(see `backend/README.md`) — the top-right status pill will show
"Backend connected" once it can reach the API.

## Pointing at a different backend

Edit the `<meta>` tag near the top of `index.html`:

```html
<meta name="backend-url" content="http://127.0.0.1:8000" />
```

Change it to wherever your backend is deployed, e.g.
`https://your-api.onrender.com`.

## Folder guide

```
frontend/
├── index.html          # page structure only — all 8 views (Dashboard,
│                        # Forecasting, Analytics, Scenario, Upload,
│                        # Knowledge, Agents, Reports) live here as
│                        # <section class="view"> blocks
├── css/
│   ├── variables.css    # colors, spacing, fonts — change theme here
│   ├── layout.css       # sidebar, topbar, grid system
│   └── components.css   # cards, buttons, tables, chat, dropzone, sliders
└── js/
    ├── config.js         # backend URL
    ├── api.js            # every fetch() call to the backend, in one place
    ├── charts.js         # shared Chart.js helpers
    ├── nav.js             # sidebar view-switching + lazy page init
    ├── dashboard.js       # Dashboard page logic
    ├── forecasting.js     # Forecasting page logic
    ├── analytics.js       # Analytics page logic
    ├── scenario.js        # Scenario Simulator page logic
    ├── upload.js          # Data Upload (drag & drop) page logic
    ├── knowledge.js       # Knowledge Base / RAG chat page logic
    ├── agents.js          # AI Agents info page (static, describes real agents)
    ├── history.js         # Reports & History page logic
    └── main.js            # backend connectivity check on load
```

## Adding a new page

1. Add a `<section class="view" id="view-yourpage">…</section>` block in
   `index.html`.
2. Add a matching sidebar button: `<button class="nav-item" data-view="yourpage">…`
3. Create `js/yourpage.js` with a `loadYourPage()` function.
4. Add a `case "yourpage": loadYourPage(); break;` inside `initView()` in
   `nav.js`, and add a label in `CRUMB_LABELS`.
5. Add `<script src="js/yourpage.js"></script>` in `index.html` (before
   `nav.js`, after `api.js`).

## Why no framework?

For a hackathon, zero build tooling means zero setup friction — anyone can
open `index.html` and it just works. If you want to port this to
React/Vue later, `js/api.js` is already a clean data layer you can reuse
as-is.
