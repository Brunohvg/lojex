from ninja import Schema
from datetime import datetime
from typing import Optional

class UsuarioIn(Schema):
    """
    Schema para entrada de dados ao criar ou atualizar um usuário.

    Atributos:
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        senha (Optional[str]): Senha do usuário (opcional), utilizada somente na criação/atualização.
    """
    nome: str
    email: str
    senha: Optional[str] = None

class UsuarioOut(Schema):
    """
    Schema para saída dos dados do usuário.

    Atributos:
        id (int): Identificador único do usuário.
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        data_criacao (datetime): Data de criação do usuário.
        data_atualizacao (datetime): Data da última atualização do usuário.
        is_active (bool): Indica se o usuário está ativo.
        is_staff (bool): Indica se o usuário possui permissões de staff.
        is_superuser (bool): Indica se o usuário é um superusuário.
    """
    id: int
    nome: str
    email: str
    data_criacao: datetime
    data_atualizacao: datetime
    is_active: bool
    is_staff: bool
    is_superuser: bool

    class Config:
        """
        Configurações adicionais para o schema.

        Atributos:
            orm_mode (bool): Permite converter instâncias ORM (como objetos do Django) para o schema.
        """
        orm_mode = True

class ErrorResponse(Schema):
    """
    Schema para padronizar as respostas de erro.

    Atributos:
        detail (str): Mensagem detalhada do erro.
    """
    detail: str
