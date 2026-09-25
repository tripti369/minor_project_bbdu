"""
RAG Agent (lightweight)

Provides simple retrieval over local text files using a lightweight
term-frequency / IDF scoring (no external ML dependencies).

This file is intentionally self-contained so it won't change other files.
"""
from pathlib import Path
from typing import Dict, List, Tuple
import math
import json
import re


def _tokenize(text: str) -> List[str]:
    # Simple tokenizer: lowercase, split on non-word characters
    return re.findall(r"\w+", text.lower())


class RAGAgent:
    """A minimal Retrieval-Augmented-Generation helper that indexes
    local documents (plain text / markdown / json) and returns relevant
    passages for a query.

    Usage:
        agent = RAGAgent()
        agent.build_index()  # scans data/knowledge, data/kb, docs
        hits = agent.search('renewal risk vendor contracts')
        answer = agent.answer('renewal risk vendor contracts')
    """

    def __init__(self, kb_paths: List[Path] = None):
        self.project_root = Path(__file__).resolve().parent.parent
        self.results = {}

        default_candidates = [
            self.project_root / "data" / "knowledge",
            self.project_root / "data" / "kb",
            self.project_root / "docs",
            self.project_root / "knowledge",
        ]

        if kb_paths:
            self.candidates = [Path(p) for p in kb_paths]
        else:
            self.candidates = default_candidates

        self.docs = {}
        self.index = {}
        self.doc_lengths = {}
        self.idf = {}
        self.indexed = False

        self.cache_dir = self.project_root / ".cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.index_file = self.cache_dir / "rag_index.json"

    def _read_file(self, path: Path) -> str:
        try:
            return path.read_text(encoding='utf-8')
        except Exception:
            return path.read_bytes().decode('utf-8', errors='ignore')

    def discover_documents(self) -> List[Path]:
        """Return a list of file paths under candidate knowledge locations."""
        files: List[Path] = []
        for cand in self.candidates:
            if not cand.exists():
                continue
            for p in cand.rglob('*'):
                if p.is_file() and p.suffix.lower() in {'.txt', '.md', '.json', '.csv'}:
                    files.append(p)
        return files

    def build_index(self, rebuild: bool = False) -> None:
        """Build or load the index. If a cached index exists and rebuild is False,
        attempt to load it for faster startup.
        """
        if self.index_file.exists() and not rebuild:
            try:
                payload = json.loads(self.index_file.read_text(encoding='utf-8'))
                self.docs = payload.get('docs', {})
                self.index = payload.get('index', {})
                self.doc_lengths = payload.get('doc_lengths', {})
                self.idf = payload.get('idf', {})
                self.indexed = True
                return
            except Exception:
                pass

        files = self.discover_documents()
        self.docs = {}
        self.index = {}
        self.doc_lengths = {}

        for f in files:
            doc_id = str(f.relative_to(self.project_root))
            text = self._read_file(f)
            if f.suffix.lower() == '.json':
                try:
                    obj = json.loads(text)
                    if isinstance(obj, dict):
                        text = ' '.join(str(v) for v in obj.values())
                    elif isinstance(obj, list):
                        text = ' '.join(str(x) for x in obj)
                except Exception:
                    pass

            self.docs[doc_id] = text
            tokens = _tokenize(text)
            self.doc_lengths[doc_id] = len(tokens)
            counts: Dict[str, int] = {}
            for t in tokens:
                counts[t] = counts.get(t, 0) + 1
            for term, tf in counts.items():
                term_entry = self.index.setdefault(term, {})
                term_entry[doc_id] = tf

        N = max(1, len(self.docs))
        self.idf = {}
        for term, postings in self.index.items():
            df = len(postings)
            self.idf[term] = math.log((N + 1) / (df + 1)) + 1.0

        try:
            payload = {
                'docs': self.docs,
                'index': self.index,
                'doc_lengths': self.doc_lengths,
                'idf': self.idf,
            }
            self.index_file.write_text(json.dumps(payload), encoding='utf-8')
        except Exception:
            pass

        self.indexed = True

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Search the indexed documents and return a list of (doc_id, score)."""
        if not self.indexed:
            self.build_index()

        qtokens = _tokenize(query)
        scores: Dict[str, float] = {}
        for t in qtokens:
            postings = self.index.get(t)
            if not postings:
                continue
            idf = self.idf.get(t, 1.0)
            for doc_id, tf in postings.items():
                scores[doc_id] = scores.get(doc_id, 0.0) + (tf * idf)

        for doc_id in list(scores.keys()):
            length = max(1, self.doc_lengths.get(doc_id, 1))
            scores[doc_id] = scores[doc_id] / math.sqrt(length)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def _make_excerpt(self, text: str, query: str, width: int = 300) -> str:
        qtokens = _tokenize(query)
        lower = text.lower()
        idx = None
        for token in qtokens:
            i = lower.find(token)
            if i >= 0:
                idx = i
                break
        if idx is None:
            return text[:width].strip() + ('...' if len(text) > width else '')
        start = max(0, idx - width // 4)
        end = min(len(text), start + width)
        excerpt = text[start:end].strip()
        if start > 0:
            excerpt = '...' + excerpt
        if end < len(text):
            excerpt = excerpt + '...'
        return excerpt

    def answer(self, query: str, top_k: int = 3) -> Dict[str, object]:
        """Return a simple RAG-style response with retrieved documents."""
        hits = self.search(query, top_k=top_k)
        results = []
        for doc_id, score in hits:
            text = self.docs.get(doc_id, "")
            excerpt = self._make_excerpt(text, query)
            results.append({
                'doc_id': doc_id,
                'score': float(score),
                'excerpt': excerpt,
            })
        response = {
            'query': query,
            'results': results,
        }
        self.results[query] = response
        return response


if __name__ == '__main__':
    agent = RAGAgent()
    agent.build_index()
    print('Indexed documents:', len(agent.docs))
    q = 'renewal risk vendor contracts'
    out = agent.answer(q)
    print(json.dumps(out, indent=2))
