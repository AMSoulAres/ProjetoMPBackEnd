# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app


client = TestClient(app)

""" ---------------------------- Teste Get ---------------------------- """


def test_lista_grupos():
    """"Teste"""
    response = client.get("/Grupos/lista-grupos")
    assert response.status_code == 200
