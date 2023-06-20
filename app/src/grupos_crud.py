"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.grupo_model import GrupoModel, GrupoUpdateModel
from app.src.models.login_model import Login
from app.src.config_db import bancoAtlax
from app.src import exceptions

router = APIRouter(
    prefix="/Grupos",
    tags=["Grupos"],
    responses={404: {"description": "Not Found"}}
)


"""         CREATE GRUPOS           """
@router.post("/criar-grupo")
async def criar_grupos(dados: GrupoModel, usuario: Login):
    """Cria um grupo"""
    if (usuario.username == "admin" and usuario.senha == 123456):
        grupos = bancoAtlax.reference("/Grupos").get()
        total_id = bancoAtlax.reference("/Grupos/Total").child("num").get()
        dados.id = total_id + 1  # incrementa id
        body = json.loads(dados.json())

        for key, grupo_existente in grupos.items():
            if key == "Total":
                break

            if dados.nome == grupo_existente['nome']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Erro: Grupo de nome {dados.nome} já existe."
                )

        bancoAtlax.reference("/Usuarios").push(body)
        bancoAtlax.reference("/Usuarios").child("Total").update({"num" : dados.id})

        return JSONResponse(
            status_code=201,
            content={"message": "Grupo adicionado com sucesso!"}
        )
    else:
        return JSONResponse(
            status_code=400,
            content={"message": "Erro: Usuário não é admin."}
        )


@router.get("/lista-grupos")
async def lista_grupos():
    """Retorna todos os grupos registrados"""
    path = bancoAtlax.reference("/Grupos")
    return path.get()
