"""Importando módulos básicos para conexão com DBcd"""
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.src.utils.busca_usuario import busca_usuario_id
from app.src.models.preferenciasgeral_model import PreferenciasGeralModel
from app.src.config_db import bancoAtlax

router = APIRouter(
    prefix="/relatorio",
    tags=["Relatório"]
)

@router.get("/{id_usuario}")
async def relatorio(id_usuario: int):

    usuarios = bancoAtlax.reference("/Usuarios").get()
    usuario_base = busca_usuario_id(id_usuario, usuarios)

    if usuario_base["admin"] == 1:
        total_usuarios = 0
        total_preferencias = 0
        total_grupos = 0
        total_chat_privado = 0
        total_chat_geral = 0
        for usuario in usuarios.values():
            total_usuarios += 1

        preferencias = bancoAtlax.reference("/Preferencias").get()
        
    return preferencias["preferencias"]
