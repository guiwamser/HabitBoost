from fastapi import APIRouter

from api.v1.endpoints import usuario
from api.v1.endpoints import habito

api_router = APIRouter()

#/api/v1/alunos
api_router.include_router(usuario.router, prefix='/usuarios', tags=["usuarios"])
api_router.include_router(habito.router, prefix='/habitos', tags=["habitos"])