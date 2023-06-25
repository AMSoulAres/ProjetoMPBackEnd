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
    response = client.post("/Preferencias/criar-preferencias/admin/Romance")
    assert response.status_code == 201
    assert response.json() == {
        "message": "Preferência criada com sucesso!"
    }


""" ------------------------- TESTE DELETE -------------------------"""
def test_deleta_grupo_sucesso():
    """Teste"""
    response = client.delete("/Grupos/deletar-preferencias/admin/Romance")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Preferência deletada com sucesso."
    }
