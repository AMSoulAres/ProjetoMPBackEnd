"""Exceções"""
from fastapi.exceptions import HTTPException
from app.src import exceptions


def busca_grupo_id(id_grupo, grupos):
    """Realiza busca de grupo por id
    Assertiva de entrada: id_grupo - id do grupo procurado
                          grupos - lista de grupos
    Assertiva de saída: grupo - grupo encontrado ou erro 404 (NotFound)  
    """
    if id_grupo is None:
        raise exceptions.ERRO_CAMPO

    for key, grupo in grupos.items():
        if key == "Total":
            break

        if id_grupo == grupo['id']:
            return grupo

    raise HTTPException(
                status_code=404,
                detail=f"Erro: Grupo de id {id_grupo} não encontrado."
                )
