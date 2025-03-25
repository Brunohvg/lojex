from ninja import Schema
from datetime import datetime
from typing import Optional

# Schema para entrada de dados ao criar/atualizar usuário
class UsuarioIn(Schema):
    nome: str
    email: str
    senha: Optional[str] = None  # senha é opcional e utilizada somente para criação/atualização

# Schema para saída dos dados do usuário
class UsuarioOut(Schema):
    id: int
    nome: str
    email: str
    data_criacao: datetime
    data_atualizacao: datetime
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        orm_mode = True  # Permite converter instâncias ORM (do Django) para o schema


class ErrorResponse(Schema):
    detail: str
