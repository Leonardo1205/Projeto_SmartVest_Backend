from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.retriever import similarity_search
from app.services.llm import answer_with_llm

router = APIRouter(tags=["chat"])

class ChatRequest(BaseModel):
    slug: str
    question: str

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        hits = similarity_search(req.slug, req.question, k=4) 
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not hits:
        return {"answer": "Não encontrei nada sobre isso neste tópico.", "chunks": []}

    top_texts = [h["text"] for h in hits]

    answer = answer_with_llm(req.question, top_texts)

    sections = list(set(h["section"] for h in hits))

    return {
        "answer": answer,
        "chunks": hits,  
        "section": sections[0] if sections else "Geral" 
    }
