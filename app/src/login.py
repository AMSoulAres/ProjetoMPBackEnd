"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.usuarios import Usuario
from app.src.config_db import bancoAtlax
from app.src import exceptions

router = APIRouter(
    prefix="/Login",
    tags=["Login"],
    responses={404: {"description": "Not Found"}}
)

@router.post("/Login")
def login_usuario(username: str, senha: int):
    usuarios  = usuarios = bancoAtlax.reference("/Usuarios").get()

    if username is None or username == "" or senha is None or senha == 0:
        raise exceptions.ERRO_CAMPO

    for usuario in usuarios.values():
        if username == usuario["username"]:
            if senha == usuario["senha"]:
                return JSONResponse(status_code=200,
                                    content={"message": "sucesso"})
            else:
                return HTTPException(status_code=400,
                                     detail= {"message": "Senha inválida"})
        else:
            return HTTPException(status_code=404,
                                 detail={"message": f"Usuário de nome {username} não encontrado."})
