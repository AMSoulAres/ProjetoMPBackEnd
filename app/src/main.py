"""Importando módulos básicos para conexão com DBcd"""
from fastapi import FastAPI
import app.src.usuarios_crud as usuarios_API
import app.src.login as login_API
import uvicorn

app = FastAPI()

app.include_router(usuarios_API.router)
app.include_router(login_API.router)
