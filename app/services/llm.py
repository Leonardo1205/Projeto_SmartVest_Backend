import os
from app.core.config import settings
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

SYSTEM_PT = (
    "Você é um assistente educacional de finanças. "
    "Responda apenas com base nos trechos fornecidos (contexto). "
    "Se não houver informação suficiente no contexto, diga exatamente: "
    "\"Não há informação suficiente neste tópico para responder com segurança.\" "
    "Seja objetivo, didático e responda em no máximo 3 frases curtas."
)

_gemini_ready = False
_model = None

def _ensure_gemini():
    global _gemini_ready, _model
    if _gemini_ready:
        return
    api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada no .env")

    genai.configure(api_key=api_key)
    model_name = (settings.GEMINI_MODEL
                or os.getenv("GEMINI_MODEL")
                or "gemini-2.5-flash")

    _model = genai.GenerativeModel(
        model_name,
        system_instruction=SYSTEM_PT,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )
    _gemini_ready = True

def _safe_extract_text(resp) -> str:
    try:
        if getattr(resp, "text", None):
            t = resp.text.strip()
            if t:
                return t
    except Exception:
        pass

    try:
        if resp and getattr(resp, "candidates", None) and resp.candidates:
            cand = resp.candidates[0]
            fr_name = getattr(cand, "finish_reason", "UNKNOWN")
            fr = cand.finish_reason.value
            
            if fr_name == "SAFETY":
                return "Não foi possível gerar a resposta (bloqueio de segurança)."
                
            parts_texts = []
            content = getattr(cand, "content", None)
            if content and getattr(content, "parts", None):
                for p in content.parts:
                    t = getattr(p, "text", None)
                    if t:
                        parts_texts.append(t)
            if parts_texts:
                return "\n".join(parts_texts).strip()
            
            if getattr(resp, "prompt_feedback", None):
                if getattr(resp.prompt_feedback, "block_reason", None):
                    return f"Não foi possível gerar a resposta (prompt bloqueado: {resp.prompt_feedback.block_reason})."

            return f"Não foi possível gerar a resposta para essa colocação."
    except Exception as e:
        return f"Não foi possível gerar a resposta para essa colocação."

    return "Não foi possível gerar a resposta (retorno vazio)."

def _call_gemini(context_chunks, question, max_output_tokens, take_n):
    ctx = "\n".join(f"- {c}" for c in context_chunks[:take_n])
    
    prompt = (
        f"**Contexto:**\n{ctx}\n\n"
        f"**Pergunta:** {question}\n"
    )
    
    resp = _model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": max_output_tokens,
            "candidate_count": 1,
            "response_mime_type": "text/plain",
        },
    )
    return resp

def _answer_with_gemini(question: str, context_chunks: list[str]) -> str:
    _ensure_gemini()

    try:
        resp = _call_gemini(context_chunks, question, max_output_tokens=512, take_n=4)
        txt = _safe_extract_text(resp)
        return txt
    except Exception as e:
         return f"Falha ao gerar resposta (gemini): {e}"

def answer_with_llm(question: str, context_chunks: list[str]) -> str:
    try:
        return _answer_with_gemini(question, context_chunks)
    except Exception as e:
        return f"Falha ao gerar resposta (gemini): {e}"