"""Importando módulos básicos para conexão com DB"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.usuario_model import UsuarioModel, UsuarioUpdateModel
from app.src.config_db import bancoAtlax
from app.src import exceptions

router = APIRouter(
    prefix="/Usuarios",
    tags=["Usuarios"],
    responses={404: {"description": "Not Found"}}
)

@router.get("/lista-usuarios")
async def lista_usuarios():
    """Lista usuarios"""
    path = bancoAtlax.reference("/Usuarios")

    return path.get()

@router.get("/lista-usuario-por-id/{id_usuario}")
async def lista_usuario_por_id(
        id_usuario: int
        ):
    """Busca um usuario por id"""
    usuarios = bancoAtlax.reference("/Usuarios").get()

    if id_usuario is None:
        raise exceptions.ERRO_CAMPO

    for key, usuario in usuarios.items():
        if key == "Total":
            break

        if id_usuario == usuario['id']:
            return usuario

    raise HTTPException(
                status_code=404,
                detail= f"Erro: Usuário de id {id_usuario} não encontrado."
                )

@router.get("/lista-usuario-por-username/{username}")
async def lista_usuario_por_username(
        username: str
        ):
    """Busca um usuario por id"""
    usuarios = bancoAtlax.reference("/Usuarios").get()

    if username is None:
        raise exceptions.ERRO_CAMPO

    for key, usuario in usuarios.items():
        if key == "Total":
            break

        if username == usuario['username']:
            return usuario
        
    raise HTTPException(
                status_code=404,
                detail= f"Erro: Usuário de username {username} não encontrado."
                )

@router.post("/criar-usuario")
async def criar_usuario(dados: UsuarioModel):
    """Cria um usuario"""
    usuarios = bancoAtlax.reference("/Usuarios").get()
    total_id = bancoAtlax.reference("/Usuarios/Total").child("num").get()
    dados.id = total_id + 1 # incrementa id
    body = json.loads(dados.json())

    for key, usuario_existente in usuarios.items():
        if key == "Total":
            break

        if dados.username == usuario_existente['username']:
            raise HTTPException(
                status_code=400,
                detail= f"Erro: Usuário de username {dados.username} já existe."
            )

    bancoAtlax.reference("/Usuarios").push(body)
    bancoAtlax.reference("/Usuarios").child("Total").update({"num" : dados.id})

    return JSONResponse(
        status_code=201,
        content={"message" : "Usuário adicionado com sucesso!"}
    )

@router.put("/update/{id_usuario}")
async def atualizar_usuario(id_usuario: int, dados: UsuarioUpdateModel):
    """Atualiza o usuario

    Assertiva de entrada: id do usuário e json com os dados que deseja alterar,
     excluindo username e id

    Assertiva de saída: o usuario é atualizado no banco e retornado na resposta
    em caso de sucesso.

    Em caso de erro, são retornado 400 (senha inválida), 404 (Usuário não encontrado)

    """
    usuarios = bancoAtlax.reference("/Usuarios").get()

    if dados.senha == 0:
        raise exceptions.ERRO_CAMPO

    for key, usuario in usuarios.items():
        if key == "Total":
            break

        if id_usuario == usuario['id']:
            usuario_armazenado = usuario
            modelo_usuario = UsuarioModel(**usuario_armazenado)

            #Exclui os campos não preenchidos do modelo para não atualizar
            dados_atualizados = dados.dict(exclude_unset=True)
            usuario_atualizado = json.loads(modelo_usuario.copy(update=dados_atualizados).json())

            #Atualiza os dados
            bancoAtlax.reference("/Usuarios").child(str(key)).update(usuario_atualizado)

            return bancoAtlax.reference("/Usuarios").child(str(key)).get()
    raise HTTPException(status_code=404,
                        detail= {"message": "Usuario não encontrado"})

@router.delete("/deletar-usuario/{username}")
async def deletar_usuario(username: str):
    """Deleta um usuario"""
    if username is None:
        raise exceptions.ERRO_CAMPO

    usuarios = bancoAtlax.reference("/Usuarios").get()

    for key, usuario in usuarios.items():
        if key == "Total":
            break

        if username == usuario['username']:
            bancoAtlax.reference("/Usuarios").child(str(key)).delete()
            return JSONResponse(
                status_code=200,
                content={"message": "Usuário deletado com sucesso."}
                )
    raise HTTPException(
        status_code=404,
        detail="Usuário não encontrado."
    )
