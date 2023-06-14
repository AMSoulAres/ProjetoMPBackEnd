"""Importando módulos básicos para conexão com DBcd"""
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
        id_usuario: Optional[int] = None
        ):
    """Busca um usuario por id"""
    usuarios = bancoAtlax.reference("/Usuarios").get()

    if id_usuario is None:
        raise exceptions.ERRO_CAMPO

    for usuario in usuarios.values():
        if id_usuario == usuario['id']:
            return usuario
    raise HTTPException(
                status_code=404,
                detail= f"Erro: Usuário de id {id_usuario} não encontrado."
                )

@router.post("/criar-usuario")
async def criar_usuario(dados: UsuarioModel):
    """Cria um usuario"""
    body = json.loads(dados.json())
    usuarios = bancoAtlax.reference("/Usuarios").get()

    if dados.id == 0:
        raise HTTPException(
                status_code=400,
                detail= "Erro: Usuário deve conter id diferente de 0"
            )

    for usuario_existente in usuarios.values():
        if dados.id == usuario_existente['id']:
            raise HTTPException(
                status_code=400,
                detail= f"Erro: Usuário de id {dados.id} já existe."
            )

    path = bancoAtlax.reference("/Usuarios")
    path.push(body)

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

@router.delete("/deletar-usuario/{id_usuario}")
async def deletar_usuario(id_usuario: int):
    """Deleta um usuario"""
    if id_usuario is None:
        raise exceptions.ERRO_CAMPO
    usuarios = bancoAtlax.reference("/Usuarios").get()
    for key, usuario in usuarios.items():
        if id_usuario == usuario['id']:
            bancoAtlax.reference("/Usuarios").child(str(key)).delete()
            return JSONResponse(
                status_code=200,
                content={"message": "Usuário deletado com sucesso."}
                )
    raise HTTPException(
        status_code=404,
        detail="Usuário não encontrado."
    )
    