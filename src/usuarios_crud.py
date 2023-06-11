"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.models.usuarios import Usuario
from src.config_db import bancoAtlax
import src.exceptions as exceptions

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

    if (id_usuario is None):
        raise exceptions.ERRO_CAMPO
    
    for usuario in usuarios.values():
        if (id_usuario == usuario['id']):
            return usuario
        else:
            raise HTTPException(
                        status_code=404,
                        detail= f"Erro: Usuário de id {id_usuario} não encontrado."
                        )

@router.post("/criar-usuario")
async def criar_usuario(usuario: Usuario):
    """Cria um usuario"""
    body = json.loads(usuario.json())
    usuarios = bancoAtlax.reference("/Usuarios").get()

    if (usuario.id == 0):
        raise HTTPException(
                status_code=400,
                detail= f"Erro: Usuário deve conter id diferente de 0"
            )
    
    for usuarioExistente in usuarios.values():
        print(usuarioExistente)
        if (usuario.id == usuarioExistente['id']):
            raise HTTPException(
                status_code=400,
                detail= f"Erro: Usuário de id {usuario.id} já existe."
            )
        
    path = bancoAtlax.reference("/Usuarios")
    path.push(body)

    return JSONResponse(
        status_code=201,
        content={"message" : "Usuário adicionado com sucesso!"}
    )

@router.delete("/deletar-usuario/{id_usuario}")
async def deletar_usuario(id_usuario: int):
    """Deleta um usuario"""
    if (id_usuario == None):
        raise exceptions.ERRO_CAMPO
    usuarios = bancoAtlax.reference("/Usuarios").get()
    for key, usuario in usuarios.items():
        if (id_usuario == usuario['id']):
            bancoAtlax.reference(f"/Usuarios").child(str(key)).delete()
            return JSONResponse(
                status_code=200,
                content={"message": "Usuário deletado com sucesso."}
                )
    raise HTTPException(
        status_code=404,
        detail="Usuário não encontrado."
    )
    