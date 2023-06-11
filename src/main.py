"""Importando módulos básicos para conexão com DBcd"""
from fastapi import FastAPI
import src.usuarios_crud as usuarios_API

app = FastAPI()

app.include_router(usuarios_API.router)
