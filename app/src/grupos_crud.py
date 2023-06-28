"""Importando módulos básicos para conexão com DBcd"""
import json
from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.src.models.grupo_model import GrupoModel
from app.src.config_db import bancoAtlax
from app.src import exceptions
from app.src.utils.busca_grupo import busca_grupo_id, busca_grupo_nome

router = APIRouter(
    prefix="/Grupos",
    tags=["Grupos"],
    responses={404: {"description": "Not Found"}}
)


""" ------------------------- CREATE -------------------------"""


@router.post("/criar-grupo/{username}")
async def criar_grupo(dados: GrupoModel, username: str):
    """Cria um Grupo
    Assertivas de Entrada: Username do usuário, para checar
    se é admin, dados em formato json.

    Assertiva de saída: O grupo é criado no banco de dados.

    Em caso de erro retorna: 404(Usuário não encontrado.),
    399(Usuário não é admin.), 400(Grupo de nome nome_do_grupo
    já existente.)"""

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
            status_code=399,
            detail="Erro: Usuário não é admin."
        )

    grupos = bancoAtlax.reference("/Grupos").get()
    total_id = bancoAtlax.reference("/Grupos/Total").child("num").get()
    dados.id = total_id + 1  # incrementa id
    body = json.loads(dados.json())

    for key, grupo_existente in grupos.items():
        if key == "Total":
            break

        if dados.nome == grupo_existente['nome']:
            raise HTTPException(
                status_code=400,
                detail=f"Erro: Grupo de nome {dados.nome} já existe."
            )

    bancoAtlax.reference("/Grupos").push(body)
    bancoAtlax.reference("/Grupos").child("Total").update({"num" : dados.id})

    return JSONResponse(
        status_code=201,
        content={"message": "Grupo criado com sucesso!"}
    )


""" ------------------------- READ -------------------------"""


@router.get("/lista-grupos")
async def lista_grupos():
    """Lista Grupos.

    Assertiva de entrada: /lista-grupos

    Assertiva de saída: Grupos armazenados na base de dados."""

    path = bancoAtlax.reference("/Grupos")
    return path.get()


@router.get("/busca-grupos-por-id/{id_grupo}")
async def busca_grupos_por_id(id_grupo: int):
    """Busca Grupo por ID.

    Assertiva de entrada: ID do Grupo.

    Assertiva de saída: Grupo procurado.

    Em caso de erro retorna 404(Grupo de id 'id_grupo'
    não encontrado.)"""
    grupos = bancoAtlax.reference("/Grupos").get()
    try:
        return busca_grupo_id(id_grupo, grupos)

    except HTTPException as exception:
        raise exception


@router.get("/busca-grupos-por-nome/{nome_grupo}")
async def busca_grupos_por_nome(nome_grupo: str):
    """Busca Grupo por nome.

    Assertiva de entrada: Nome do grupo.

    Assertiva de saída: Grupo procurado.

    Em caso de erro retorn 404(Grupo de nome
    'nome_grupo' não encontrado.)"""
    grupos = bancoAtlax.reference("/Grupos").get()
    try:
        return busca_grupo_nome(nome_grupo, grupos)

    except HTTPException as exception:
        raise exception


@router.get("/lista-grupos-por-preferencia/{preferencia}")
async def lista_grupos_por_preferencia(preferencia: str):
    """Lista grupos por preferência.

    Assertiva de entrada: Preferência à ser pesquisada.

    Assertiva de saída: Lista de nomes de grupos com a
    preferencia desejada.

    Em caso de erro retorna 404(Nenhum grupo encontrado.)"""

    grupos = bancoAtlax.reference("/Grupos").get()
    resultado = []
    if preferencia is None:
        raise exceptions.ERRO_CAMPO
    for key, grupo in grupos.items():
        if key == "Total":
            break
        if preferencia in grupo['preferencias']:
            resultado.append(grupo)
    if resultado == []:
        raise HTTPException(
            status_code=404,
            detail="Nenhum grupo encontrado."
        )
    return resultado

@router.get("/lista-membros/{nome_grupo}")
async def grupo_lista_membros(nome_grupo: str):
    """Lista membros de um grupo.

    Assertiva de entrada: Nome do grupo.

    Assertiva de saída: Membros do grupo.

    Em caso de erro retorna 404(Grupo não encontrado.)."""
    grupos = bancoAtlax.reference("/Grupos").get()
    if nome_grupo is None:
        raise exceptions.ERRO_CAMPO
    for key, grupo in grupos.items():
        if key == "Total":
            break
        if nome_grupo == grupo['nome']:
            return grupo['membros']
    raise HTTPException(
        status_code=404,
        detail="Grupo não encontrado."
    )


""" ------------------------- UPDATE -------------------------"""


@router.put("/atualizar-grupo/remover-membro/{username}/{nome_grupo}/{username_removido}")
async def atualizar_grupo_remover_membro(username: str, nome_grupo: str,
                                         username_removido: str):
    """Remove um membro de um grupo.

    Assertiva de entrada: username do usuario, nome do grupo, username do
    usuario à ser removido.

    Assertiva de saída: o grupo é atualizado no banco e retornado na resposta
    em caso de sucesso.

    Em caso de erro retorna 404(Usuário não encontrado.), 404(Grupo não encontrado.),
    399(Usuário não é admin.).
    """
    admin = 0
    usuarios = bancoAtlax.reference("/Usuarios").get()
    grupos = bancoAtlax.reference("/Grupos").get()

    if username is None:
        raise exceptions.ERRO_CAMPO
    if nome_grupo is None:
        raise exceptions.ERRO_CAMPO

    for key, usuario in usuarios.items():
        if key == "Total":
            break

        if username == usuario['username']:
            if usuario['id'] == 1:
                admin = 1
    if admin == 0:
        raise HTTPException(
            status_code=399,
            detail="Erro: Usuário não é admin."
        )
    for key, grupo in grupos.items():
        if key == "Total":
            break

        if nome_grupo == grupo['nome']:
            for membro in grupo['membros']:
                if membro == username_removido:
                    grupo['membros'].remove(username_removido)
                    grupo_atualizado = grupo
                    bancoAtlax.reference("/Grupos").child(str(key)).update(grupo_atualizado)
                    return bancoAtlax.reference("/Grupos").child(str(key)).get()
            raise HTTPException(status_code=404,
                                detail="Erro: Membro não encontrado.")
    raise HTTPException(status_code=404,
                        detail="Erro: Grupo não encontrado.")


@router.put("/atualizar-grupo/adicionar-membro/{username}/{nome_grupo}/{username_adicionado}")
async def atualizar_grupo_adicionar_membro(username: str, nome_grupo: str,
                                           username_adicionado: str):
    """Adiciona um membro à um grupo.

    Assertiva de entrada: username do usuario, nome do grupo, username do
    usuario à ser adicionado.

    Assertiva de saída: o grupo é atualizado no banco e retornado na resposta
    em caso de sucesso.

    Em caso de erro retorna 404(Grupo não encontrado.), 400(Membro já
    registrado no grupo.), 399(Usuário não é admin.).
    """
    admin = 0
    usuarios = bancoAtlax.reference("/Usuarios").get()
    grupos = bancoAtlax.reference("/Grupos").get()

    if username is None:
        raise exceptions.ERRO_CAMPO
    if nome_grupo is None:
        raise exceptions.ERRO_CAMPO

    for key, usuario in usuarios.items():
        if key == "Total":
            break

        if username == usuario['username']:
            if usuario['id'] == 1:
                admin = 1
    if admin == 0:
        raise HTTPException(
            status_code=399,
            detail="Erro: Usuário não é admin."
        )
    for key, grupo in grupos.items():
        if key == "Total":
            break

        if nome_grupo == grupo['nome']:
            for membro in grupo['membros']:
                if membro == username_adicionado:
                    raise HTTPException(
                        status_code=400,
                        detail="Erro: Membro já registrado no grupo."
                    )
            grupo['membros'].append(username_adicionado)
            grupo_atualizado = grupo
            bancoAtlax.reference("/Grupos").child(str(key)).update(grupo_atualizado)
            return bancoAtlax.reference("/Grupos").child(str(key)).get()
    raise HTTPException(status_code=404,
                        detail="Erro: Grupo não encontrado.")


""" ------------------------- DELETE -------------------------"""


@router.delete("/deletar-grupo/{username}/{nome_grupo}")
async def deletar_grupo(nome_grupo: str, username: str):
    """Deleta o grupo se o usuário for admin e o grupo for válido.

    Assertivas de Entrada: Nome do usuário, nome do grupo.

    Assertivas de Saída: O grupo é deletado no banco de dados.

    Em caso de erro retorna 404 (Grupo não encontrado.), 404 (Usuário não
    encontrado.), 399 (Usuário não é admin.)."""

    admin = 0
    usuarios = bancoAtlax.reference("/Usuarios").get()
    grupos = bancoAtlax.reference("/Grupos").get()

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
            status_code=399,
            detail="Erro: Usuário não é admin."
        )

    for key, grupo in grupos.items():
        if key == "Total":
            break

        if nome_grupo == grupo['nome']:
            bancoAtlax.reference("/Grupos").child(str(key)).delete()
            return JSONResponse(
                status_code=200,
                content={"message": "Grupo deletado com sucesso."}
                )
    raise HTTPException(
        status_code=404,
        detail="Grupo não encontrado."
    )


