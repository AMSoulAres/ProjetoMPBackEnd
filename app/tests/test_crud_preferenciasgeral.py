# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

""" ----------------------------Teste get------------------------------------ """
def test_preferencias_geral_sucesso():
    """"Teste"""
    response = client.get("/Preferencias/preferencias-geral")
    assert response.status_code == 200
    assert response.json()


def test_preferencias_geral_erro():
    """"Teste"""
    response = client.get("/Preferencias/preferenciasgeral")
    assert response.status_code == 404
    assert response.json()