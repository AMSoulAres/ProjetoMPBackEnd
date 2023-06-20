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


"""" Teste Create """


def teste_grupo_criar_grupo_falha():
    """ Teste """
    response = client.post("/Grupos/criar-grupo",
                           json={
                               "id": 99,
                               "nome": "terror",
                               "usuarios": ["junior", "joao", "jose"],
                               "preferencias": ["terror", "horror", "suspense"]
                           })
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
