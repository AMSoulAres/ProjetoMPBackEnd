"""Importando módulos básicos para conexão com DBcd"""
import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.preferenciasgeral_model import PreferenciasGeralModel
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
    """Cria uma preferência se o usuário for admin e se a
    Preferência não exisir.
    Assertivas de Entrada: Username do usuário, para checar
    se é admin, dados em formato json.

    Assertiva de saída: A preferência é criada na lista de
    preferência do banco de dados.

    Em caso de erro retorna: 401(Usuário não é admin.),
    409(Preferência já existe)."""
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

        if preferencia_existente['NomePreferencias'] == dados.NomePreferencias:
            raise HTTPException(
                status_code=409,
                detail=f"Erro: Preferência {preferencia_existente['NomePreferencias']} já existe."
            )

    total_id = bancoAtlax.reference("/Preferencias/Total").child("num").get()
    body = json.loads(dados.json())

    bancoAtlax.reference("/Preferencias").push(body)
    bancoAtlax.reference("/Preferencias").child("Total").update({"num" : total_id + 1})

    return JSONResponse(
        status_code=201,
        content={"message": "Preferência criada com sucesso!"}
    )



""" ------------------------- READ -------------------------"""
@router.get("/preferencias-geral")
async def preferencias_geral():
    """Lista Preferências Geral.

    Assertiva de entrada: /preferencias-geral

    Assertiva de saída: Preferências armazenadas
    na base de dados."""

    path = bancoAtlax.reference("/Preferencias")
    return path.get()

@router.get("/lista-preferencias")
async def lista_preferencias():
    """Lista Preferências Geral.

    Assertiva de entrada: /preferencias-geral

    Assertiva de saída: Preferências armazenadas
    na base de dados."""
    lista_preferencias = []
    preferencias = bancoAtlax.reference("/Preferencias").get()
    for key, preferencia in preferencias.items():
        if key == "Total":
            pass

        lista_preferencias.append(preferencia["NomePreferencias"])

    return lista_preferencias



""" ------------------------- DELETE -------------------------"""
@router.delete("/deletar-preferencias/{username}/{nome_preferencia}")
async def deletar_preferencias(username: str, nome_preferencia: str):
    """Deleta uma preferência se o usuário for admin e a preferência for válida.
    Assertivas de Entrada: Nome de usuário, dados em formato json.

    Assertiva de saída: A preferência é deletada da lista de
    preferência do banco de dados.

    Em caso de erro retorna: 401(Usuário não é admin.),
    409(Preferência não existe)."""
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
    if nome_preferencia is None:
        raise exceptions.ERRO_CAMPO

    for key, preferencia_existente in preferencias.items():
        if key == "Total":
            break

        if preferencia_existente['NomePreferencias'] == nome_preferencia:
            bancoAtlax.reference("/Preferencias").child(str(key)).delete()
            return JSONResponse(
                status_code=200,
                content={"message": "Preferência deletada com sucesso!"}
            )
    raise HTTPException(
        status_code=404,
        detail=f"Erro: Preferência {nome_preferencia} não existe."
    )
