from pathlib import Path
import json
from sentence_transformers import SentenceTransformer
import faiss
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data" / "topics"
INDEX_DIR = BASE.parents[0] / "db" / "vector"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def load_markdown(slug: str) -> str:
    fp = DATA_DIR / slug / "content.md"
    if not fp.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {fp}")
    return fp.read_text(encoding="utf-8")

def chunk_text_with_sections(text: str):
    """Divide por headings do Markdown e depois fatia em chunks menores.
       Retorna dois arrays paralelos: chunks, metas (com 'section')."""
    md = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
    )
    docs = md.split_text(text)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150,  
        separators=["\n\n", "\n", ". ", " "],
    )

    chunks, metas = [], []
    for d in docs:
        section = d.metadata.get("h3") or d.metadata.get("h2") or d.metadata.get("h1") or "Geral"
        parts = splitter.split_text(d.page_content)
        for p in parts:
            if p and p.strip():
                chunks.append(p.strip())
                metas.append({"section": section})
    return chunks, metas

def build_index(slug: str):
    text = load_markdown(slug)
    chunks, metas = chunk_text_with_sections(text)
    if not chunks:
        raise ValueError("Nenhum chunk gerado - verifique content.md")

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  
    index.add(embeddings)

    out_dir = INDEX_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(out_dir / "index.faiss"))
    (out_dir / "meta.json").write_text(
        json.dumps({"chunks": chunks, "meta": metas}, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"[OK] Índice criado em: {out_dir}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python -m app.services.ingest_topic <slug>")
        sys.exit(1)
    build_index(sys.argv[1])
