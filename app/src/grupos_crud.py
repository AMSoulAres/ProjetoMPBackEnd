"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.grupo_model import GrupoModel, GrupoUpdateModel
from app.src.config_db import bancoAtlax
from app.src import exceptions


router = APIRouter(
    prefix="/Grupos",
    tags=["Grupos"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/lista-grupos")
async def lista_grupos():
    "Retorna todos os grupos registrados"
    path = bancoAtlax.reference("/Grupos")
    return path.get()
