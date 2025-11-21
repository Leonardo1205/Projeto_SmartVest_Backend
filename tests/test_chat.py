from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_chat_endpoint_mocked():
    payload = {
        "slug": "renda-fixa-vs-variavel",
        "question": "O que é renda fixa?"
    }

    with patch("app.api.v1.routes.chat.similarity_search") as mock_search, \
         patch("app.api.v1.routes.chat.answer_with_llm") as mock_llm:

        mock_search.return_value = [
            {"text": "Renda fixa é segura...", "section": "Definição", "score": 0.9}
        ]
        mock_llm.return_value = "Renda fixa é um tipo de investimento onde..."

        response = client.post("/api/v1/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        
        assert data["answer"] == "Renda fixa é um tipo de investimento onde..."
        assert data["section"] == "Definição"