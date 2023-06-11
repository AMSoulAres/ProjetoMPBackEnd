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

app = FastAPI()

""" ----------- Get, Post, Put e Delete Usuarios --------------- """
@app.get("/lista-usuários")
async def lista_usuarios():
    path = bancoAtlax.reference("/Usuarios")
    return path.get()

@app.get("/lista-usuario-por-id/{id_usuario}")
async def lista_usuario_por_id(
        id_usuario: Optional[int] = None
        ):
    usuarios = bancoAtlax.reference("/Usuarios").get()
    if (id_usuario == None):
        return exceptions.ERRO_CAMPO
    for usuario in usuarios.values():
        if (id_usuario != None):
            if (id_usuario == usuario['id']):
                return usuario
            else:
                return JSONResponse(
                            status_code=404,
                            content={"message": f"Erro: Usuário de id {id_usuario}"}
                            )
    return exceptions.ERRO_NAO_ESPERADO

@app.post("/criar-usuario")
async def criar_usuario(usuario: Usuario):
    try:
        path = bancoAtlax.reference("/Usuarios")
        body = json.loads(usuario.json())
        path.push(body)
        return JSONResponse(
            status_code=201,
            content={"message" : "Usuário adicionado com sucesso!"}
        )
    except:
        return JSONResponse(
            status_code=901,
            content={"message": "Erro inesperado"})
    
@app.delete("/deletar-usuario")
async def deletar_usuario(id_usuario: int):
        if (id_usuario == None):
            return exceptions.ERRO_CAMPO
        usuarios = bancoAtlax.reference("/Usuarios").get()
        for key, usuario in usuarios.items():
            if (id_usuario == usuario['id']):
                bancoAtlax.reference(f"/Usuarios").child(str(key)).delete()
                return JSONResponse(
                    status_code=200,
                    content={"message": "Usuário deletado com sucesso."}
                    )
        return JSONResponse(
            status_code=404,
            content={"message": "Usuário não encontrado."}
        )
        
