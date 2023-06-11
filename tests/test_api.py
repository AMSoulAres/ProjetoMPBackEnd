"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_lista_usuarios_sucesso():
    """Teste"""
    response = client.get("/Usuarios/lista-usuarios")
    assert response.status_code == 200
    assert response.json()

def test_lista_usuarios_erro():
    """Teste"""
    response = client.get("/Usuarios/listausuarios")
    assert response.status_code == 404
    assert response.json()

def test_lista_usuario_por_id_sucesso():
    """Teste"""
    response = client.get("/Usuarios/lista-usuario-por-id/1")
    assert response.status_code == 200
    assert response.json() == { "admin": 1,
                                "id": 1,
                                "senha": 12346,
                                "username": "admin"
                                }

def test_lista_usuario_por_id_erro_404():
    """Teste"""
    response = client.get("/Usuarios/lista-usuario-por-id/0")
    assert response.status_code == 404
    assert response.json() == {
                    "detail": "Erro: Usuário de id 0 não encontrado.",
                    }

def test_criar_usuario_sucesso():
    """Teste"""
    response = client.post("/Usuarios/criar-usuario",
                         json={
                            "id": 999,
                            "username": "string",
                            "senha": 999999,
                            "admin": 0,
                            "preferencias": [0],
                            "amigos": [1],
                            "bloqueados": [0],
                            "grupos": [0]
                            }
                        )
    assert response.status_code == 201
    assert response.json() == {
                    "message": "Usuário adicionado com sucesso!",
                    }
# Deleta o usuário após teste para poder executar novamente
    client.delete("/Usuarios/deletar-usuario/999")

def test_deletar_usuario_erro_ja_existe():
    """Teste"""
    response = client.post("/Usuarios/criar-usuario",
                         json={
                            "id": 1,
                            "username": "string",
                            "senha": 999999,
                            "admin": 0,
                            "preferencias": [0],
                            "amigos": [1],
                            "bloqueados": [0],
                            "grupos": [0]
                            }
                        )
    assert response.status_code == 400
    assert response.json() == {
                        "detail": "Erro: Usuário de id 1 já existe."
                        }

def test_deletar_usuario_erro_0():
    """Teste"""
    response = client.post("/Usuarios/criar-usuario",
                         json={
                            "id": 0,
                            "username": "string",
                            "senha": 999999,
                            "admin": 0,
                            "preferencias": [0],
                            "amigos": [1],
                            "bloqueados": [0],
                            "grupos": [0]
                            }
                        )
    assert response.status_code == 400
    assert response.json() == {
                        "detail": "Erro: Usuário deve conter id diferente de 0"
                        }

def test_deletar_usuario_sucesso():
    """Teste"""
    client.post("/Usuarios/criar-usuario",
                         json={
                            "id": 989,
                            "username": "string",
                            "senha": 999999,
                            "admin": 0,
                            "preferencias": [0],
                            "amigos": [1],
                            "bloqueados": [0],
                            "grupos": [0]
                            }
                        )
    response = client.delete("/Usuarios/deletar-usuario/1")
    assert response.status_code == 200
