from ninja import Schema
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict, field_validator  # Import necessário para compatibilidade

class LojaIn(Schema):
    """
    Schema para entrada de dados ao criar ou atualizar um loja.
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validate_cnpj])
    endereco = models.TextField()
    telefone = models.CharField(max_length=11, validators=[validate_telefone])
    criado_em = models.DateTimeField(auto_now_add=True)

    """
    nome: Optional[str] = None  # Torna o nome opcional
    cnpj: Optional[str] = None  # Torna o nome opcional
    endereco: Optional[str] = None  # Torna o nome opcional
    telefone: Optional[str] = None  # Torna o nome opcional
    criado_em: Optional[datetime] = None  # Torna o nome opcional

    @field_validator("nome", "cnpj", "endereco", "telefone", mode="before")
    @classmethod
    def validar_str(cls, v):
        if not isinstance(v, str):
            raise ValueError("O campo deve ser uma string")
        return v.strip()


class LojaOut(Schema):
    id: int
    nome: str
    cnpj: str
    endereco: str
    telefone: str
    criado_em: datetime


    model_config = ConfigDict(from_attributes=True)  # Substitui orm_mode

class ErrorResponse(Schema):
    detail: str