# pylint: disable=pointless-string-statement
"""Modulos importando o FastAPI"""
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)

""" ------------------------- TESTE GET -------------------------  """

def test_busca_mensagem_por_id_sucesso():
    """Teste"""
    response = client.get("/ChatGrupo/grupos_mensagens/1/mensagens/")
    assert response.status_code == 404
    assert response.json()

def test_busca_mensagem_idgrupo_erro():
    """Teste"""
    response = client.get("/ChatGrupo/grupos_mensagens/1000000/mensagens/")
    assert response.status_code == 404
    assert response.json()

def test_usuario_no_grupo():
    """Teste"""
    response = client.get("/ChatGrupo/usuario_grupo/254/5/")
    assert response.status_code == 404
    assert response.json()

def test_enviar_grupo_menssage():
    """Teste"""
    response = client.post("/grupos_mensagens/254/5/", {"id": 5, "timestamp":"string", "mensagem": "Olá!"})
    assert response.status_code == 200
    assert response.json() == {'mensagem enviada com sucesso!'}

def test_atualizar_existencia_grupo():
    # Teste para verificar se o grupo é atualizado com sucesso.
    response = client.put("/grupos/1/")
    assert response.status_code == 200
    assert response.json() == grupos_mensagens[1]
    
    # Teste para verificar se o grupo é excluído com sucesso.
    response = client.put("/grupos/2/")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Erro: Grupo não existe mais.'}
