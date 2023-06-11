from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: int
    username: str
    senha: int
    admin: Optional[int] = 0
    preferencias: list
    amigos: list
    bloqueados: list
    grupos: list