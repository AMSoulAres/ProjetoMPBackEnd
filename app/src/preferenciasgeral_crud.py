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

""" ------------------------- CREATE -------------------------"""
@router.post("/criar-preferencias/{username}")
async def criar_preferencias(dados: PreferenciasGeralModel, username: str):
    """Cria uma preferência
    Assertivas de Entrada: Nome da preferência, que deve
    ser checada se já existe ou não, dados em formato json.

    Assertiva de saída: A preferência é criada na lista de
    preferência do banco de dados.

    Em caso de erro retorna: 402(Usuário não é admin.)"""
    admin = 0
    usuarios = bancoAtlax.reference("/Usuarios").get()
    if username is None:
        raise exceptions.ERRO_CAMPO

    for key, usuario in usuarios.items():
        if key == "Total":
            break

        if username == usuario['username']:
            if usuario['id'] == 1:
                admin = 1
    if admin == 0:
        raise HTTPException(
            status_code=401,
            detail="Erro: Usuário não é admin."
        )

    preferencias = bancoAtlax.reference("/Preferencias").get()
    if dados.NomePreferencias is None:
        raise exceptions.ERRO_CAMPO

    for key, preferencia_existente in preferencias.items():
        if key == "Total":
            break

        if preferencia_existente == dados.NomePreferencias:
            raise HTTPException(
                status_code=409,
                detail=f"Erro: Preferência {preferencia_existente} já existente."
            )
        
    total_id = bancoAtlax.reference("/Preferencias/Total").child("num").get()
    body = json.loads(dados.json())

    bancoAtlax.reference("/Preferencias").push(body)
    bancoAtlax.reference("/Preferencias").child("Total").update({"num" : total_id + 1})

    return JSONResponse(
        status_code=201,
        content={"message": "Preferência criada com sucesso!"}
    )