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
from app.src.utils.busca_grupo import busca_grupo_id, busca_grupo_nome

router = APIRouter(
    prefix="/Grupos",
    tags=["Grupos"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/lista-grupos")
async def lista_grupos():
    """Lista Grupos"""

    path = bancoAtlax.reference("/Grupos")
    return path.get()


@router.get("/busca-grupos-por-id/{id_grupo}")
async def busca_grupos_por_id(id_grupo: int):
    """Busca Grupo por ID"""
    grupos = bancoAtlax.reference("/Grupos").get()
    try:
        return busca_grupo_id(id_grupo, grupos)

    except HTTPException as exception:
        raise exception


@router.get("/busca-grupos-por-nome/{nome_grupo}")
async def busca_grupos_por_nome(nome_grupo: str):
    """Busca Grupo por nome"""
    grupos = bancoAtlax.reference("/Grupos").get()
    try:
        return busca_grupo_nome(nome_grupo, grupos)
    
    except HTTPException as exception:
        raise exception
