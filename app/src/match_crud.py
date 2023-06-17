"""Importando módulos básicos para conexão com DB"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.match_models import MatchUsuarioGrupoModel, MatchUsuarioGrupoModelUpdate
from app.src.models.match_models import MatchUsuarioModel, MatchUsuarioModelUpdate
from app.src import exceptions

router = APIRouter(
    prefix="/Match",
    tags=["Match"],
    responses={404: {"description": "Not Found"}}
)


# @router.get("/lista-match", response_model=list[])
# async def get_usuarios():