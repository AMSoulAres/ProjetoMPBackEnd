"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

def test_login_sucesso():
    """Teste de login"""
    response = client.post("/Login",
                         json={
                            "username": "string",
                            "senha": 999999,
                            }
                        )
    assert response.status_code == 200