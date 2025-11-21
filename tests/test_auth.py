from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_login_success():
    login_data = {
        "email": "teste@email.com",
        "password": "senha123"
    }

    with patch("app.api.v1.routes.auth.auth_service.authenticate") as mock_auth:
        
        mock_auth.return_value = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.TOKEN_FALSO"

        response = client.post("/api/v1/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["access_token"] == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.TOKEN_FALSO"

def test_register_success():
    user_data = {
        "nickname": "Novo Usuario",
        "email": "novo@email.com",
        "password": "senhaforte123"
    }

    with patch("app.api.v1.routes.auth.user_service.register") as mock_reg, \
         patch("app.api.v1.routes.auth.auth_service.authenticate") as mock_auth:
        
        from app.schemas.user import UserRead
        mock_reg.return_value = UserRead(id=1, nickname="Novo Usuario", email="novo@email.com")
        mock_auth.return_value = "TOKEN_DE_REGISTRO"

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 201
        assert response.json()["access_token"] == "TOKEN_DE_REGISTRO"