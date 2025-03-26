from ninja import Router
from .schemas import LojaIn, LojaOut, ErrorResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Loja
from typing import List
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
router = Router(tags=["Lojas"])

@router.get("/", response=List[LojaOut])
def listar_lojas(request):
    try:
        lojas = Loja.objects.all()
        return [LojaOut.model_validate(loja) for loja in lojas]
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao listar lojas: " + str(e))

@router.get("/{loja_id}", response={200: LojaOut, 404: ErrorResponse})
def obter_loja(request, loja_id: int):
    try:
        loja = Loja.objects.get(id=loja_id)
        return LojaOut.model_validate(loja)
    except ObjectDoesNotExist:
        return 404, ErrorResponse(detail="Loja não encontrada")
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao obter loja: " + str(e))
    
@router.post("/", response={201: LojaOut, 400: ErrorResponse})
def criar_loja(request, loja: LojaIn):
    try:
        data = loja.model_dump()
        loja_obj = Loja.objects.create(**data)
        return 201, LojaOut.model_validate(loja_obj)
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao criar loja: " + str(e))
    
@router.put("/{loja_id}", response={200: LojaOut, 404: ErrorResponse})
def atualizar_loja(request, loja_id: int, data: LojaIn):
    try:
        loja_obj = Loja.objects.get(id=loja_id)
        data_dict = data.model_dump()
        for key, value in data_dict.items():
            setattr(loja_obj, key, value)
        loja_obj.save()
        return LojaOut.model_validate(loja_obj)
    except ObjectDoesNotExist:
        return 404, ErrorResponse(detail="Loja não encontrada")
    except Exception as e:
        return 500, ErrorResponse(detail="Erro ao atualizar loja: " + str(e))
    
@router.delete("/{loja_id}", response={204: None, 404: ErrorResponse, 500: ErrorResponse})
def deletar_loja(request, loja_id: int):
    try:
        loja = get_object_or_404(Loja, id=loja_id)  # Retorna 404 se a loja não existir
        loja.delete()

        # Verifica se a loja realmente foi deletada
        if Loja.objects.filter(id=loja_id).exists():
            return 500, ErrorResponse(detail="Erro ao deletar a loja do banco de dados.")

        return HttpResponse(status=204)  # Retorna corretamente o 204
    except Exception as e:
        return 500, ErrorResponse(detail=f"Erro ao deletar loja: {str(e)}")