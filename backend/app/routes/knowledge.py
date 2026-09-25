"""
/api/knowledge
==============
RAG-style search across the markdown knowledge base in data/knowledge/,
used by the frontend's "Ask Enterprise AI" chat box.
"""

from fastapi import APIRouter, Query

from app.agents.rag_agent import RAGAgent

router = APIRouter()
rag_agent = RAGAgent()
rag_agent.build_index()


@router.get("/knowledge")
def knowledge(q: str = Query("", description="Natural language question")):
    if not q.strip():
        return {"query": q, "results": []}
    return rag_agent.answer(q, top_k=3)
