"""from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioSchema(BaseModel):
    id: int
    nome: str
    email: EmailStr
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True  # Permite que o Pydantic converta os objetos ORM do Django em dicts

class CriarUsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str  # A senha não será retornada, mas será usada na criação do usuário

    class Config:
        orm_mode = True
"""