/* =========================================================
   main.js
   App bootstrap: pings the backend once on load so the top
   status pill accurately shows "Backend connected" or
   "Backend offline" instead of always claiming success.
========================================================= */

async function checkBackendConnection() {
  const pill = document.getElementById("statusPill");
  if (!pill) return;
  try {
    await API.health();
    pill.innerHTML = '<span class="dot"></span> Backend connected';
    pill.className = "status-pill";
  } catch (err) {
    pill.innerHTML = '<span class="dot"></span> Backend offline';
    pill.className = "status-pill";
    pill.style.background = "var(--color-danger-soft)";
    pill.style.color = "#ffb3b0";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  checkBackendConnection();
});
