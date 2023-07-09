"""Importando módulos básicos para conexão com DBcd"""
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.chatgrupo_model import GrupoMensagemModel, MensagemModel
from app.src.config_db import bancoAtlax
from app.src.utils.busca_grupo import busca_grupo_id
from app.src.utils.busca_usuario import busca_usuario_id
from datetime import datetime

router = APIRouter(
    prefix="/ChatGrupo",
    tags=["Chat Grupo"],
    responses={404: {"description": "Not Found"}}
)

grupos_mensagens = {}

""" ------------------------- READ -------------------------"""
@router.get("/grupos_mensagens/{idGrupo}/mensagens/")
async def buscar_grupo_message(idGrupo: int):
    """Busca mensagens existentes no grupo

    Assertiva de entrada: id do grupo.

    Assertiva de saída:Retorna as mensagens do idgrupo.
    """
    grupos = bancoAtlax.reference("/Grupos").get()

    try:
        busca_grupo_id(idGrupo, grupos)
        if idGrupo not in grupos_mensagens:
            grupos_mensagens[idGrupo] = []
        return grupos_mensagens[idGrupo] 
     
    except HTTPException as exception:
        raise exception
        


@router.get("/usuario_grupo/{idGrupo}/{idUsuario}/")
async def usuario_no_grupo(idGrupo: int, idUsuario: int):
    """Verificar se idUsuario é um membro do grupo.

    Assertiva de entrada: id do grupo, e id do usuario.

    Assertiva de saída: Retorna um erro se o usuario não tiver no grupo, e True se tiver."""

    grupos = bancoAtlax.reference("/Grupos").get()
    usuarios = bancoAtlax.reference("/Usuarios").get()

    try:
        busca_grupo_id(idGrupo, grupos)
        busca_usuario_id(idUsuario, usuarios)

        usuario = busca_usuario_id(idUsuario, usuarios)
        grupo = busca_grupo_id(idGrupo, grupos)
        membros_grupo = grupo["membros"]
        nome_usuario = usuario["username"]
        
        if nome_usuario not in membros_grupo:
            raise HTTPException(status_code=404, detail="Erro: O usuário não pode enviar mensagem, pois não está no grupo.")
        return True
    except HTTPException as exception:
        raise exception

""" ------------------------- CREATE -------------------------"""

@router.post("/grupos_mensagens/{idGrupo}/{idUsuario}/", response_model=MensagemModel)
async def enviar_grupo_menssage(idGrupo: int, idUsuario:int, Mensagens: MensagemModel):
    """ Enviar mensagem para o grupo

    Assertiva de entrada: id do grupo,id do usuario, e modelo de dados armazenados em MensagemModel.

    Assertiva de saída:Retorna uma mensagem de sucesso caso a mensagem seja enviada."""

    grupos = bancoAtlax.reference("/Grupos").get()
    usuarios = bancoAtlax.reference("/Usuarios").get()

    try:
        
        busca_grupo_id(idGrupo, grupos)
        busca_usuario_id(idUsuario, usuarios)
        usuario_no_grupo(idGrupo, idUsuario)

        if idGrupo not in grupos_mensagens:
            grupos_mensagens[idGrupo] = []

        total_id = bancoAtlax.reference("/ChatGrupo/Total").child("num").get()

        Mensagens.timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        Mensagens.idUsuario = idUsuario
        grupos_mensagens[idGrupo].append(Mensagens)
        grupos_mensagens[idGrupo] = sorted(grupos_mensagens[idGrupo], key=lambda x: x['timestamp'])
        
        bancoAtlax.reference("/ChatGrupo").child("Total").update({"num": total_id + 1})
        return {'mensagem enviada com sucesso!'}

    except HTTPException as exception:
        raise exception    
        
    

