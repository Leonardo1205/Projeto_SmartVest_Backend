from pathlib import Path
import json
import faiss
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).resolve().parents[1]
INDEX_DIR = BASE.parents[0] / "db" / "vector"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def load_index(slug: str):
    d = INDEX_DIR / slug
    idx_path = d / "index.faiss"
    meta_path = d / "meta.json"
    if not idx_path.exists() or not meta_path.exists():
        raise FileNotFoundError("Índice do tópico não encontrado. Rode o ingest.")
    index = faiss.read_index(str(idx_path))
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    chunks = meta["chunks"]
    metas = meta.get("meta", [{"section": "Geral"} for _ in chunks])
    return index, chunks, metas

def similarity_search(slug: str, question: str, k=4):
    model = get_model()
    index, chunks, metas = load_index(slug)
    q_vec = model.encode([question], convert_to_numpy=True, normalize_embeddings=True)
    D, I = index.search(q_vec, k)
    hits = []
    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        hits.append({"score": float(score), "text": chunks[idx], "section": metas[idx].get("section", "Geral")})
    return hits
