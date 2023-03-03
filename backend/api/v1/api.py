from fastapi import APIRouter

from api.v1.endpoints import usuario
from api.v1.endpoints import tarefa

api_router = APIRouter()

#/api/v1/alunos
api_router.include_router(usuario.router, prefix='/usuarios', tags=["usuarios"])
api_router.include_router(tarefa.router, prefix='/tarefas', tags=["tarefas"])