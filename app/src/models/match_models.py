# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
"""Modulos para definição do modelo"""
from typing import Optional
from pydantic import BaseModel

class MatchUsuarioGrupoModel(BaseModel):
    """Modelo json match de usuario com um grupo"""
    idUsuario: int
    idGrupo: int
    match: float

class MatchUsuarioModel(BaseModel):
    """Modelo json match de usuario com outro usuario"""
    idUsuarioR: int
    idUsuarioD: int
    match: float

class MatchUsuarioGrupoModelUpdate(BaseModel):
    """Modelo json para atualização match de usuario com um grupo"""
    idUsuarioR: Optional[int]
    idGrupo: Optional[int]
    match: Optional[float]

class MatchUsuarioModelUpdate(BaseModel):
    """Modelo json para atualização match de usuario com um grupo"""
    idUsuarioR: Optional[int]
    idUsuarioD: Optional[int]
    match: Optional[float]
