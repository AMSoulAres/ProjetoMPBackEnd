"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from src.configDB import bancoAtlax
from fastapi import FastAPI, Request, Path, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from firebase_admin import credentials, auth
from src.models.usuarios import Usuario
import src.exceptions as exceptions

app = FastAPI()

""" ----------- Get, Post, Put e Delete Usuarios --------------- """
@app.get("/lista-usuários")
async def lista_usuarios():
    path = bancoAtlax.reference("/Usuarios")
    return path.get()

@app.get("/lista-usuario-por-id/{usuario_id}")
async def lista_usuario_por_id(
        usuario_id: Optional[int] = None
        ):
    usuarios = bancoAtlax.reference("/Usuarios").get()
    if (usuario_id == None):
        return exceptions.ERRO_CAMPO
    for usuario in usuarios.values():
        if (usuario_id != None):
            if (usuario_id == usuario['id']):
                return usuario
            else:
                return JSONResponse(
                            status_code=404,
                            content={"message": f"Erro: Usuário de id {usuario_id}"}
                            )
    return exceptions.ERRO_NAO_ESPERADO

@app.post("/criar-usuario")
async def criar_usuario(usuario: Usuario):
    try:
        path = bancoAtlax.reference("/Usuarios")
        body = json.loads(usuario.json())
        path.child('Usuarios').push(body)
        return JSONResponse(
            status_code=201,
            content={"message" : "Usuário adicionado com sucesso!"}
        )
    except:
        return JSONResponse(
            status_code=901,
            content={"message": "Erro inesperado"})
