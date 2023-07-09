"""Importando módulos básicos para conexão com DBcd"""
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.chatPrivado_model import ChatPrivadoModel
from app.src.config_db import bancoAtlax
from app.src import exceptions
from datetime import datetime
from app.src.utils.busca_usuario import busca_usuario_id

router = APIRouter(
    prefix="/ChatPrivado",
    tags=["Chat Privado"],
    responses={404: {"description": "Not Found"}}
)

""" ------------------------- READ -------------------------"""


@router.get("/buscar-mensagens/{idRUsuario}/{idDUsuario}")
async def buscar_mensagens(idRUsuario: int, idDUsuario: int):
        
    usuarios = bancoAtlax.reference("/Usuarios").get()
    try:
        busca_usuario_id(idRUsuario, usuarios)
        busca_usuario_id(idDUsuario, usuarios)
        todasMensagens = bancoAtlax.reference('/ChatPrivado').get()
        listaMensagens = []
        
        
        for key, mensagem in todasMensagens.items():
            try:
                if mensagem["idRUsuario"] == idDUsuario and mensagem["idDUsuario"] == idRUsuario or mensagem["idRUsuario"] == idRUsuario and mensagem["idDUsuario"] == idDUsuario:
                    listaMensagens.append(mensagem)
                
            except KeyError:
                pass
        sorted_list = sorted(listaMensagens, key=lambda k: k["timestamp"])
        return listaMensagens

    except HTTPException as exception:
        raise exception
    

""" ------------------------- CREATE -------------------------"""


@router.post("/enviar-mensagem")
async def enviar_mensagem(dados: ChatPrivadoModel):

    usuarios = bancoAtlax.reference("/Usuarios").get()
    try:
        busca_usuario_id(dados.idRUsuario, usuarios)
        busca_usuario_id(dados.idDUsuario, usuarios)
        total_id = bancoAtlax.reference("/ChatPrivado/Total").child("num").get()
        body = json.loads(dados.json())
        body["timestamp"] = datetime.now()
        
        bancoAtlax.reference("/ChatPrivado").push(body)
        bancoAtlax.reference("/ChatPrivado").child("Total").update({"num": total_id + 1})
        
        return JSONResponse(
            status_code =201,
            content= {"message": "Mensagem enviada com sucesso!"}
        )
    except HTTPException as exception:
        raise exception