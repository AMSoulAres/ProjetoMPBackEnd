"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.usuario_model import UsuarioModel, UsuarioUpdateModel
from app.src.config_db import bancoAtlax
from app.src import exceptions

