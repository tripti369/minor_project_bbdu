"""
RAG Agent — ChromaDB vector database backend
Indexes local knowledge documents (data/knowledge/*.md) using ChromaDB
with a lightweight character n-gram embedding. No API key needed.
"""
from pathlib import Path
from typing import Dict, List, Tuple
import re
import json

import chromadb


class RAGAgent:
    """RAG helper backed by a local ChromaDB vector database.

    Usage:
        agent = RAGAgent()
        agent.build_index()
        result = agent.answer('why do customers churn')
    """

    def __init__(self, kb_paths: List[Path] = None):
        self.project_root = Path(__file__).resolve().parent.parent.parent  # backend/
        self.results = {}

        default_candidates = [self.project_root / "data" / "knowledge"]
        self.candidates = [Path(p) for p in kb_paths] if kb_paths else default_candidates

        # ChromaDB persistent client — stores vectors in data/chroma/
        chroma_dir = str(self.project_root / "data" / "chroma")
        self._client = chromadb.PersistentClient(path=chroma_dir)
        self._collection = self._client.get_or_create_collection(
            name="rag_knowledge",
            metadata={"hnsw:space": "cosine"},
        )
        self.docs: Dict[str, str] = {}
        self.indexed = False

    def _read_file(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except Exception:
            return path.read_bytes().decode("utf-8", errors="ignore")

    def discover_documents(self) -> List[Path]:
        files: List[Path] = []
        for cand in self.candidates:
            if not cand.exists():
                continue
            for p in cand.rglob("*"):
                if p.is_file() and p.suffix.lower() in {".txt", ".md", ".json"}:
                    files.append(p)
        return files

    def build_index(self, rebuild: bool = True) -> None:
        """Index documents into ChromaDB.
        rebuild=True (default) ensures knowledge base edits are always picked up.
        """
        # Another RAG agent may rebuild the shared collection during startup.
        # Re-acquire the handle before using it so this instance is never stale.
        self._collection = self._client.get_or_create_collection(
            name="rag_knowledge",
            metadata={"hnsw:space": "cosine"},
        )
        existing = self._collection.count()
        if existing > 0 and not rebuild:
            all_items = self._collection.get(include=["documents"])
            for doc_id, text in zip(all_items["ids"], all_items["documents"]):
                self.docs[doc_id] = text
            self.indexed = True
            return

        if rebuild and existing > 0:
            self._client.delete_collection("rag_knowledge")
            self._collection = self._client.get_or_create_collection(
                name="rag_knowledge",
                metadata={"hnsw:space": "cosine"},
            )

        files = self.discover_documents()
        self.docs = {}

        ids, documents, metadatas = [], [], []
        for f in files:
            doc_id = str(f.relative_to(self.project_root))
            text = self._read_file(f)
            self.docs[doc_id] = text
            ids.append(doc_id)
            documents.append(text[:2000])
            metadatas.append({"source": doc_id})

        if ids:
            self._collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

        self.indexed = True

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        self._collection = self._client.get_or_create_collection(
            name="rag_knowledge",
            metadata={"hnsw:space": "cosine"},
        )
        if not self.indexed:
            self.build_index(rebuild=False)

        results = self._collection.query(
            query_texts=[query],
            n_results=min(top_k, max(1, self._collection.count())),
            include=["distances", "documents"],
        )
        hits = []
        for doc_id, dist in zip(results["ids"][0], results["distances"][0]):
            score = round(1.0 - dist, 4)
            hits.append((doc_id, score))
        return hits

    def _make_excerpt(self, text: str, query: str, width: int = 320) -> str:
        lower = text.lower()
        idx = None
        for token in re.findall(r"\w+", query.lower()):
            i = lower.find(token)
            if i >= 0:
                idx = i
                break
        if idx is None:
            return text[:width].strip() + ("..." if len(text) > width else "")
        start = max(0, idx - width // 4)
        end = min(len(text), start + width)
        excerpt = text[start:end].strip()
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(text):
            excerpt += "..."
        return excerpt

    def answer(self, query: str, top_k: int = 3) -> Dict[str, object]:
        hits = self.search(query, top_k=top_k)
        results = []
        for doc_id, score in hits:
            text = self.docs.get(doc_id, "")
            results.append({
                "doc_id": doc_id,
                "score": round(float(score), 3),
                "excerpt": self._make_excerpt(text, query),
            })
        response = {"query": query, "results": results}
        self.results[query] = response
        return response
