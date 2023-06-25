# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
"""Modulos para definição do modelo"""
from typing import Optional
from pydantic import BaseModel

class Model(BaseModel):  # pylint: disable=too-few-public-methods
    """Modelo de preferencias """
    NomePreferencias: str
