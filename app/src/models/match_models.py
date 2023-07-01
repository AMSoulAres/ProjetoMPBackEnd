# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
"""Modulos para definição do modelo"""
from typing import Optional
from pydantic import BaseModel

class MatchUsuarioGrupoModel(BaseModel):
    """Modelo json match de usuario com um grupo"""
    nomeGrupo: str
    match: str

class MatchUsuarioModel(BaseModel):
    """Modelo json match de usuario com outro usuario"""
    usernameUsuario: str
    match: str