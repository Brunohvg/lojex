from ninja import Schema
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict, EmailStr, SecretStr, field_validator  # Import necessário para compatibilidade


class UsuarioIn(Schema):
    """
    Schema para entrada de dados ao criar ou atualizar um usuário.
    """
    nome: Optional[str] = None  # Torna o nome opcional
    email: Optional[EmailStr] = None  # Torna o e-mail opcional
    senha: Optional[SecretStr] = None  # Torna a senha opcional com SecretStr para proteção

    @field_validator("nome", "email", mode="before")
    @classmethod
    def validar_str(cls, v):
        if not isinstance(v, str):
            raise ValueError("O campo deve ser uma string")
        return v.strip()

    @field_validator("senha", mode="before")
    @classmethod
    def validar_senha(cls, v):
        if v is not None and not isinstance(v, str):
            raise ValueError("A senha deve ser uma string")
        return v


class UsuarioOut(Schema):
    id: int
    nome: str
    email: str
    data_criacao: datetime
    data_atualizacao: datetime
    is_active: bool
    is_staff: bool
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)  # Substitui orm_mode

class ErrorResponse(Schema):
    detail: str
