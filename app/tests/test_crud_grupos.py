# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app


client = TestClient(app)

""" ------------------------- TESTE GET -------------------------  """


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


""" ------------------------- TESTE POST ------------------------- """


def test_cria_grupo_sucesso():
    """Teste"""
    response = client.post("/Grupos/criar-grupo/admin",
                           json={
                               "id": 99,
                               "nome": "Teste",
                               "membros": ["Testinho", "Testão"],
                               "preferencias": ["Testezada"]
                           })
    assert response.status_code == 201
    assert response.json() == {
        "message": "Grupo criado com sucesso!"
    }


def test_cria_grupo_erro_nao_admin():
    """Teste"""
    response = client.post("/Grupos/criar-grupo/0",
                           json={
                              "id": 22,
                              "nome": "Ação",
                              "membros": ["Julio, Julia"],
                              "preferencias": ["Ação"]
                            })
    assert response.status_code == 399
    assert response.json() == {
        "detail": "Erro: Usuário não é admin."
    }


def test_cria_grupo_erro_nome_existente():
    """Teste"""
    response = client.post("/Grupos/criar-grupo/admin",
                           json={
                               "id": 22,
                               "nome": "qualquernome",
                               "membros": ["Jubileu", "Carminha"],
                               "preferencias": ["Ação"]
                               })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Erro: Grupo de nome qualquernome já existe."
    }


def test_grupo_adicionar_membro_sucesso():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/adicionar-membro/admin/Romance/Faustão")
    assert response.status_code == 200
    assert response.json() == {
        "id": 6,
        "membros": [
            "Jô Soares", "Faustão"
        ],
        "nome": "Romance",
        "preferencias": [
            "Romance"
        ]
    }


def test_grupo_adicionar_membro_erro_nao_admin():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/adicionar-membro/jao/Romance/Faustão")
    assert response.status_code == 399
    assert response.json() == {
        "detail": "Erro: Usuário não é admin."
    }


def test_grupo_adicionar_membro_erro_membro_ja_registrado():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/adicionar-membro/admin/Romance/Faustão")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Erro: Membro já registrado no grupo."
    }


def test_grupo_adicionar_membro_erro_grupo_nao_encontrado():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/adicionar-membro/admin/mamacos/Faustão")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Erro: Grupo não encontrado."
    }


def test_grupo_remover_membro_sucesso():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/remover-membro/admin/Romance/Faustão")
    assert response.status_code == 200
    assert response.json() == {
        "id": 6,
        "membros": [
            "Jô Soares"
        ],
        "nome": "Romance",
        "preferencias": [
            "Romance"
        ]
    }


def test_grupo_remover_membro_erro_nao_admin():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/remover-membro/joao/Romance/Ratinho")
    assert response.status_code == 399
    assert response.json() == {
        "detail": "Erro: Usuário não é admin."
    }


def test_grupo_remover_membro_erro_membro_nao_encontrado():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/remover-membro/admin/Romance/carlinhos")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Erro: Membro não encontrado."
    }


def test_grupo_remover_membro_erro_grupo_nao_encontrado():
    """Teste"""
    response = client.post("/Grupos/atualizar-grupo/remover-membro/admin/jacare/carlinhos")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Erro: Grupo não encontrado."
    }


def test_deleta_grupo_sucesso():
    """Teste"""
    response = client.post("/Grupos/deletar-grupo/admin/Teste")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Grupo deletado com sucesso."
    }


def test_deleta_grupo_nao_admin():
    """Teste"""
    response = client.post("/Grupos/deletar-grupo/usuario/acao")
    assert response.status_code == 399
    assert response.json() == {
        "detail": "Erro: Usuário não é admin."
    }


def test_deleta_grupo_nao_encontrado():
    """Teste"""
    response = client.post("/Grupos/deletar-grupo/admin/jeremias")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Grupo não encontrado."
    }
