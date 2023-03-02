from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.usuario_model import Usuario
from core.deps import get_session
from models.requests.usuario_create import UserCreateRequest

from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

router = APIRouter()

@router.get('/', response_model=List[Usuario])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario)

        result= await session.execute(query)

        usuarios: List[Usuario]= result.scalars().all()

        return usuarios

@router.get('/{usuario_id}', status_code=status.HTTP_200_OK, response_model=Usuario)
async def get_usuario(usuario_id : int , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario).filter(Usuario.id == usuario_id)
        result= await session.execute(query)
        usuario : Usuario = result.scalar_one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Usuario)
async def post_usuario(create_request: UserCreateRequest,db : AsyncSession = Depends(get_session)):
    novo_usuario = Usuario(nome=create_request.nome, fone= create_request.fone, email=create_request.email, hash_password=create_request.hash_password)

    db.add(novo_usuario)
    await db.commit()

    return novo_usuario






@router.put('/{usuario_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Usuario)
async def put_usuario(usuario_id : int, usuario: Usuario , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario).filter(Usuario.id == usuario_id)

        result= await session.execute(query)

        usuario_up : Usuario = result.scalar_one_or_none()

        if usuario_up:
            usuario_up.nome = usuario.nome
            usuario_up.fone = usuario.fone
            usuario_up.email = usuario.email
            usuario_up.password = usuario.password

            await session.commit()

            return usuario_up
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id : int , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario).filter(Usuario.id == usuario_id)

        result= await session.execute(query)

        usuario_del : Usuario = result.scalar_one_or_none()

        if usuario_del:
            await session.delete(usuario_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)