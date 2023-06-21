# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app


client = TestClient(app)

""" ---------------------------- Teste Get ---------------------------- """


def test_lista_grupos_sucesso():
    """"Teste"""
    response = client.get("/Grupos/lista-grupos")
    assert response.status_code == 200
    assert response.json()


def test_lista_grupos_erro():
    """"Teste"""
    response = client.get("/Grupos/listagrupos")
    assert response.status_code == 404
    assert response.json()


def test_busca_grupo_por_id_sucesso():
    """Teste"""
    response = client.get("/Grupos/busca-grupos-por-id/1")
    assert response.status_code == 200
    assert response.json()


def test_busca_grupo_por_id_erro():
    """Teste"""
    response = client.get("/Grupos/busca-grupos-por-id/213214")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Erro: Grupo de id 213214 não encontrado."
    }


def test_busca_grupo_por_nome_sucesso():
    """Teste"""
    response = client.get("/Grupos/busca-grupos-por-nome/grupo1")
    assert response.status_code == 200
    assert response.json()


def test_busca_grupo_por_nome_erro():
    """Teste"""
    response = client.get("/Grupos/busca-grupos-por-nome/grupo3542")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Erro: Grupo de nome grupo3542 não encontrado."
    }
