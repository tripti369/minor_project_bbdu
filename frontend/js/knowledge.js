/* =========================================================
   knowledge.js
   Knowledge Base page — a simple chat UI on top of the real
   RAG Agent (TF-IDF search over data/knowledge/*.md), called
   via GET /api/knowledge?q=...
========================================================= */

let knowledgeWired = false;

function initKnowledge() {
  if (knowledgeWired) return;
  knowledgeWired = true;

  const input = document.getElementById("ragInput");
  const askBtn = document.getElementById("ragAskBtn");
  if (askBtn) askBtn.addEventListener("click", askRag);
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") askRag();
    });
  }
}

async function askRag() {
  const input = document.getElementById("ragInput");
  const chatArea = document.getElementById("chatArea");
  if (!input || !chatArea) return;

  const query = input.value.trim();
  if (!query) return;

  const userBubble = document.createElement("div");
  userBubble.className = "chat-bubble user";
  userBubble.textContent = query;
  chatArea.appendChild(userBubble);

  const thinking = document.createElement("div");
  thinking.className = "chat-bubble ai";
  thinking.textContent = "Searching the knowledge base…";
  chatArea.appendChild(thinking);
  chatArea.scrollTop = chatArea.scrollHeight;
  input.value = "";

  try {
    const data = await API.ask(query);
    if (!data.answer) {
      thinking.textContent = "No answer found for that query.";
    } else {
      const sources = (data.sources || [])
        .map((r) => `<div class="chat-source">📄 ${r.doc_id} · score ${r.score}</div>`)
        .join("");
      thinking.innerHTML = `${data.answer}<div class="chat-source">Engine: ${data.ai_engine}</div><div style="margin-top:10px;">${sources}</div>`;
    }
  } catch (err) {
    console.error(err);
    thinking.textContent = `Unable to reach backend at ${BACKEND_URL}.`;
  }
  chatArea.scrollTop = chatArea.scrollHeight;
}
