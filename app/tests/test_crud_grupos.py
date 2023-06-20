# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app


client = TestClient(app)

""" Teste inicial """
def teste_grupo_inicial():
    """"Teste"""
    response = client.get("/Grupos/lista-grupos")
    assert response.status_code == 200
