/* =========================================================
   upload.js
   Data Upload page — drag & drop (or click) a CSV, it's sent
   to POST /api/upload where the backend classifies its type,
   stores it, logs it in the database, and returns a preview.
========================================================= */

let uploadWired = false;

function initUpload() {
  if (uploadWired) return; // only wire listeners once
  uploadWired = true;

  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("fileInput");
  if (!dropzone || !fileInput) return;

  dropzone.addEventListener("click", () => fileInput.click());

  ["dragenter", "dragover"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.add("drag");
    })
  );
  ["dragleave", "drop"].forEach((evt) =>
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.classList.remove("drag");
    })
  );
  dropzone.addEventListener("drop", (e) => {
    const files = e.dataTransfer.files;
    if (files && files.length) handleUpload(files[0]);
  });
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) handleUpload(fileInput.files[0]);
  });
}

async function handleUpload(file) {
  const statusEl = document.getElementById("uploadStatus");
  const resultCard = document.getElementById("uploadResultCard");
  if (statusEl) statusEl.textContent = `Uploading and classifying "${file.name}"…`;
  if (resultCard) resultCard.style.display = "none";

  try {
    const result = await API.upload(file);
    if (result.error) {
      if (statusEl) statusEl.textContent = `Error: ${result.error}`;
      return;
    }
    renderUploadResult(result);
    if (statusEl) statusEl.textContent = `"${file.name}" processed successfully.`;
  } catch (err) {
    console.error(err);
    if (statusEl) statusEl.textContent = `Upload failed. Is the backend running at ${BACKEND_URL}?`;
  }
}

function renderUploadResult(result) {
  const resultCard = document.getElementById("uploadResultCard");
  if (!resultCard) return;
  resultCard.style.display = "block";

  setText("uploadDetectedType", result.detected_type);
  setText("uploadConfidence", `${result.confidence}%`);
  setText("uploadRows", result.rows.toLocaleString());
  setText("uploadColumns", result.columns);
  setText("uploadNulls", result.null_count);
  setText("uploadFilename", result.filename);

  const confBar = document.getElementById("uploadConfidenceBar");
  if (confBar) confBar.style.width = `${result.confidence}%`;

  const theadRow = document.getElementById("uploadPreviewHead");
  const tbody = document.getElementById("uploadPreviewBody");
  if (theadRow && result.headers) {
    theadRow.innerHTML = result.headers.map((h) => `<th>${h}</th>`).join("");
  }
  if (tbody && result.preview) {
    tbody.innerHTML = result.preview
      .map(
        (row) =>
          `<tr>${result.headers.map((h) => `<td>${row[h] ?? ""}</td>`).join("")}</tr>`
      )
      .join("");
  }
}
