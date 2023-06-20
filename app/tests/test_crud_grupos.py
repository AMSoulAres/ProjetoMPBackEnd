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


def teste_grupo_criar_grupo_falha_usuario_nao_e_admin():
    """ Teste """
    response = client.post("/Grupos/criar-grupo",
                           json={
                               "dados": {
                                    "id": 99,
                                    "nome": "terror",
                                    "usuarios": ["junior", "joao", "jose"],
                                    "preferencias": ["terror", "horror"]
                               },
                               "usuario": {
                                   "username": "admin",
                                   "senha": 0
                               }
                           })
    assert response.status_code == 400
    assert response.json() == {"message": "Erro: Usuário não é admin."}
