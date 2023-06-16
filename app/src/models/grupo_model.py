# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
"""Modulos para definição do modelo"""
from typing import Optional
from pydantic import BaseModel


class Grupo(BaseModel):  # pylint: disable=too-few-public-methods
    """Modelo de grupo """
    id: int
    usuarios: list
    preferencias: list


class GrupoUpdate(BaseModel):  # pylint: disable=too-few-public-methods
    """Modelo de grupo"""
    usuarios: Optional[list]
