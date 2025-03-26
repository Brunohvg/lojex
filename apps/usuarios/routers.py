from ninja import Router
from typing import List
from .models import Usuario
from .schemas import UsuarioIn, UsuarioOut, ErrorResponse, UsuarioLojaIn, UsuarioLojaOut
from django.core.exceptions import ObjectDoesNotExist, ValidationError


router = Router(tags=["Usuarios"])

def validar_email_unico(email: str):
    if Usuario.objects.filter(email=email).exists():
        raise ValidationError("Usuário com este e-mail já existe")

@router.get("/", response=List[UsuarioOut])
def listar_usuarios(request):
    try:
        usuarios = Usuario.objects.all()
        return [UsuarioOut.model_validate(usuario) for usuario in usuarios]  # Usando model_validate()
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao listar usuários: " + str(e))

@router.get("/{usuario_id}", response={200: UsuarioOut, 404: ErrorResponse})
def obter_usuario(request, usuario_id: int):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        return UsuarioOut.model_validate(usuario)  # Usando model_validate()
    except ObjectDoesNotExist:
        return 404, ErrorResponse(detail="Usuário não encontrado")
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao obter usuário: " + str(e))

@router.post("/", response={201: UsuarioOut, 400: ErrorResponse})
def criar_usuario(request, usuario: UsuarioIn):
    try:
        # Validando se o email já existe
        validar_email_unico(usuario.email)
        
        data = usuario.model_dump()  # Convertendo para dicionário validado
        senha = data.pop("senha", None)

        if senha:
            senha = senha.get_secret_value()  # Obtendo a string real de SecretStr
        
        usuario_obj = Usuario.objects.create_user(senha=senha, **data)
        return 201, UsuarioOut.model_validate(usuario_obj)  # Usando model_validate()
    except ValidationError as e:
        # Tratando o erro para retornar uma string ao invés de lista
        return 400, ErrorResponse(detail=str(e.message))
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao criar usuário: " + str(e))

@router.put("/{usuario_id}", response={200: UsuarioOut, 404: ErrorResponse})
def atualizar_usuario(request, usuario_id: int, data: UsuarioIn):
    try:
        usuario_obj = Usuario.objects.get(id=usuario_id)  # Usando .get() para buscar o usuário
        
        # Convertendo para dicionário, mas tratando os campos opcionais
        data_dict = data.model_dump()  # Usando model_dump()
        senha = data_dict.pop("senha", None)

        # Atualizando os campos do usuário, mas apenas se o campo não for None
        for attr, value in data_dict.items():
            if value is not None:  # Verificando se o valor não é None antes de atribuir
                setattr(usuario_obj, attr, value)
        
        # Atualizando a senha se fornecida
        if senha:
            senha = senha.get_secret_value()  # Obtendo a senha de forma segura
            usuario_obj.set_password(senha)
        
        # Salvando as alterações
        usuario_obj.save()
        
        return 200, UsuarioOut.model_validate(usuario_obj)  # Retorna a resposta validada
    
    except ObjectDoesNotExist:
        return 404, ErrorResponse(detail="Usuário não encontrado")
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao atualizar usuário: " + str(e))
    
@router.delete("/{usuario_id}", response={200: dict, 404: ErrorResponse})
def deletar_usuario(request, usuario_id: int):
    try:
        usuario_obj = Usuario.objects.get(id=usuario_id)
        usuario_obj.delete()
        return 200, {"success": True}
    except ObjectDoesNotExist:
        return 404, ErrorResponse(detail="Usuário não encontrado")
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao deletar usuário: " + str(e))


@router.post("/loja/", response={201: UsuarioLojaOut, 400: ErrorResponse})
def adicionar_usuario_loja(request, usuario_loja: UsuarioLojaIn):
    try:
        usuario = Usuario.objects.get(id=usuario_loja.usuario_id)
        usuario.lojas.add(usuario_loja.loja_id, through_defaults={"cargo": usuario_loja.cargo})
        return 201, UsuarioLojaOut.model_validate(usuario_loja)
    except ObjectDoesNotExist:
        return 404, ErrorResponse(detail="Usuário ou loja não encontrados")
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao adicionar usuário à loja: " + str(e))
    
@router.delete("/loja/", response={204: None, 404: ErrorResponse, 500: ErrorResponse})
def remover_usuario_loja(request, usuario_loja: UsuarioLojaIn):
    try:
        usuario = Usuario.objects.get(id=usuario_loja.usuario_id)
        usuario.lojas.remove(usuario_loja.loja_id)
        return 204, None
    except ObjectDoesNotExist:
        return 404, ErrorResponse(detail="Usuário ou loja não encontrados")
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao remover usuário da loja: " + str(e))

