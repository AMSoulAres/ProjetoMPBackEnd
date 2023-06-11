"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from src.config_db import bancoAtlax
from fastapi import FastAPI, Request, Path, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from firebase_admin import credentials, auth
from src.models.usuarios import Usuario
import src.exceptions as exceptions
import src.usuarios_crud as usuarios_API

app = FastAPI()

app.include_router(usuarios_API.router)
