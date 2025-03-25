# apps/motoboys/routers.py
from ninja import Router
from typing import List
from .models import Usuario
from .schemas import UsuarioIn, UsuarioOut, ErrorResponse


router = Router(tags=["Usuarios"])

@router.get("/", response=List[UsuarioOut])
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return [UsuarioOut.from_orm(usuario) for usuario in usuarios]


@router.get("/{usuario_id}", response={200: UsuarioOut, 404: ErrorResponse})
def obter_usuario(request, usuario_id: int):
    usuario = Usuario.objects.filter(id=usuario_id).first()
    if not usuario:
        return 404, ErrorResponse(detail="Usuário não encontrado")
    return UsuarioOut.from_orm(usuario)


@router.post("/", response={201: UsuarioOut, 400: ErrorResponse})
def criar_usuario(request, usuario: UsuarioIn):
    if Usuario.objects.filter(email=usuario.email).exists():
        return 400, ErrorResponse(detail="Usuário com este e-mail já existe")
    
    data = usuario.dict()
    senha = data.pop("senha", None)
    usuario_obj = Usuario.objects.create_user(senha=senha, **data)
    return 201, UsuarioOut.from_orm(usuario_obj)


@router.put("/{usuario_id}", response={200: UsuarioOut, 404: ErrorResponse})
def atualizar_usuario(request, usuario_id: int, data: UsuarioIn):
    usuario_obj = Usuario.objects.filter(id=usuario_id).first()
    if not usuario_obj:
        return 404, ErrorResponse(detail="Usuário não encontrado")
    
    data_dict = data.dict()
    senha = data_dict.pop("senha", None)
    
    for attr, value in data_dict.items():
        setattr(usuario_obj, attr, value)
    
    if senha:
        usuario_obj.set_password(senha)
    
    usuario_obj.save()
    return 200, UsuarioOut.from_orm(usuario_obj)

@router.delete("/{usuario_id}", response={200: dict, 404: ErrorResponse})
def deletar_usuario(request, usuario_id: int):
    usuario_obj = Usuario.objects.filter(id=usuario_id).first()
    if not usuario_obj:
        return 404, ErrorResponse(detail="Usuário não encontrado")
    usuario_obj.delete()
    return 200, {"success": True}
