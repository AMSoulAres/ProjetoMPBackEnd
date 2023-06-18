# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

""" ----------------------------Teste create------------------------------------ """
def test_criar_match_usuario_sucesso():
    """Teste"""
    response = client.get("/Match/cria-match-usuario")
    assert response.status_code == 201

def test_criar_match_usuario_grupo_sucesso():
    """Teste"""
    response = client.get("/Match/cria-match-usuario-grupo")
    assert response.status_code == 200