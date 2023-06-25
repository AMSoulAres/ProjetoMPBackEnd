"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.preferenciasgeral_model import PreferenciasGeralModel
from app.src.models.login_model import Login
from app.src.config_db import bancoAtlax
from app.src import exceptions

router = APIRouter(
    prefix="/Preferencias",
    tags=["Preferencias"],
    responses={404: {"description": "Not Found"}}
)