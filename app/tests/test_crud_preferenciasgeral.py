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
    response = client.post("/Preferencias/criar-preferencias/admin",
                           json = {"NomePreferencias": "Romance"})
    assert response.status_code == 201
    assert response.json() == {
        "message": "Preferência criada com sucesso!"
    }

def test_cria_preferencias_erro_preferencia_ja_existe():
    """Teste"""
    response = client.post("/Preferencias/criar-preferencias/admin",
                           json = {"NomePreferencias": "Terror"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Erro: Preferência Terror já existe."
    }

def test_cria_preferencias_erro_nao_admin():
    """Teste"""
    response = client.post("/Preferencias/criar-preferencias/0",
                           json = {"NomePreferencias": "Romance"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Erro: Usuário não é admin."
    }


""" ------------------------- TESTE DELETE -------------------------"""
def test_deleta_preferencias_sucesso():
    """Teste"""
    response = client.delete("/Preferencias/deletar-preferencias/admin",
                           json = {"NomePreferencias": "Romance"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Preferência deletada com sucesso."
    }

def test_deleta_preferencias_erro_preferencia_ja_existe():
    """Teste"""
    response = client.post("/Preferencias/deletar-preferencias/admin",
                           json = {"NomePreferencias": "Anime"})
    assert response.status_code == 409
    assert response.json() == {
        "detail": "Erro: Preferência Anime não existe."
    }

def test_deleta_preferencias_erro_nao_admin():
    """Teste"""
    response = client.post("/Preferencias/deletar-preferencias/0",
                           json = {"NomePreferencias": "Anime"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Erro: Usuário não é admin."
    }
