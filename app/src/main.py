"""Importando módulos básicos para conexão com DBcd"""
from fastapi import FastAPI
import app.src.usuarios_crud as usuarios_API
import app.src.login as login_API
import app.src.match_crud as match_API
import app.src.grupos_crud as grupos_API
import app.src.preferenciasgeral_crud as preferencias_API


app = FastAPI()

app.include_router(usuarios_API.router)
app.include_router(login_API.router)
app.include_router(match_API.router)
app.include_router(grupos_API.router)
app.include_router(preferencias_API.router)