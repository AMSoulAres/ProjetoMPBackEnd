# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
"""Modulos para definição do modelo"""
from typing import Optional
from pydantic import BaseModel

class Usuario(BaseModel): # pylint: disable=too-few-public-methods
    """Modelo de Usuario"""
    id: int
    username: str
    senha: int
    admin: Optional[int] = 0
    preferencias: list
    amigos: list
    bloqueados: list
    grupos: list
