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


""" ------------------------- TESTE POST ------------------------- """
def test_cria_preferencias_sucesso():
    """Teste"""
    response = client.post("/Preferencias/criar-preferencias/Romance/admin")
    assert response.status_code == 201
    assert response.json() == {
        "message": "Preferência(s) criada(s) com sucesso!"
    }


def test_cria_preferencias_erro_preferencia_existente():
    """Teste"""
    response = client.post("/Grupos/criar-grupo/qualquernome/admin")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Erro: Preferência qualquernome já existe."
    }
