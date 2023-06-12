"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.login_model import Login
from app.src.config_db import bancoAtlax
from app.src import exceptions

router = APIRouter(
    prefix="/Login",
    tags=["Login"],
    responses={404: {"description": "Not Found"}}
)

@router.post("/")
def login_usuario(login_request: Login):
    usuarios = bancoAtlax.reference("/Usuarios").get()

    if (login_request.username is None or login_request.username == ""
            or login_request.senha is None or login_request.senha == 0):
        raise exceptions.ERRO_CAMPO

    for usuario in usuarios.values():
        if login_request.username == usuario["username"]:
            if login_request.senha == usuario["senha"]:
                return JSONResponse(status_code=200,
                                    content={"message": "sucesso"})
            else:
                raise HTTPException(status_code=400,
                                     detail= {"message": "Senha inválida"})
    raise HTTPException(status_code=404,
                                 detail={"message": f"Usuário de nome {login_request.username} não encontrado."})
