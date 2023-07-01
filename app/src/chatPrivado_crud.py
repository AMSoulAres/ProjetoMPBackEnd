"""Importando módulos básicos para conexão com DBcd"""
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
# from fastapi.exceptions import HTTPException
from app.src.models.chatPrivado_model import ChatPrivadoModel
from app.src.config_db import bancoAtlax
# from app.src import exceptions
from datetime import datetime

router = APIRouter(
    prefix="/ChatPrivado",
    tags=["Chat Privado"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/buscar-mensagens-total/{idUsuario}")
async def buscar_mensagens(idUsuario: int):
    todasMensagens = bancoAtlax.reference('/ChatPrivado').get()
    listaMensagens = []

    for key, mensagem in todasMensagens.items():
        try:
            if mensagem["idDUsuario"] == idUsuario or mensagem["idRUsuario"] == idUsuario:
                listaMensagens.append(mensagem)
        except KeyError:
            pass
    return listaMensagens


@router.post("/enviar-mensagem/{idRUsuario}/{idDUsuario}")
async def enviar_mensagem(dados: ChatPrivadoModel, idRUsuario: int, idDUsuario: int):
    total_id = bancoAtlax.reference("/ChatPrivado/Total").child("num").get()
    body = json.loads(dados.json())
    body["idRUsuario"] = idRUsuario
    body["idDUsuario"] = idDUsuario
    body["timestamp"] = str(datetime.now()) if body["timestamp"] == None else body["timestamp"]
    bancoAtlax.reference("/ChatPrivado").push(body)
    bancoAtlax.reference("/ChatPrivado").child("Total").update({"num" : total_id + 1})

    return JSONResponse(
        status_code=201,
        content={"message" : "Mensagem enviada com sucesso!"}
    )
    