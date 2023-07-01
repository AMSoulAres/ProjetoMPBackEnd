# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

""" ------------------------- TESTE GET -------------------------  """

def test_busca_mensagem_por_id_sucesso():
    """Teste"""
    response = client.get("/ChatPrivado/buscar-mensagens/0/1")
    assert response.status_code == 200
    assert response.json()

""" ------------------------- TESTE POST ------------------------- """

def test_cria_chat_sucesso():
    """Teste"""
    response = client.post("/ChatPrivado/enviar-mensagem/0/2",
                           json={
                                    "mensagem": "testando"
                           })
    assert response.status_code == 201
    assert response.json() == {
        "message": "Mensagem enviada com sucesso!"
    }

