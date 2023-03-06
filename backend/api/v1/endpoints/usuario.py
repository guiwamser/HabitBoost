from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Form
from fastapi import Response


from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.models import Usuario
from core.deps import get_session
from models.requests.usuario_create import UserCreateRequest
from models.responses.usuario_response import UsuarioResponse
from core.security import criar_token_jwt, verify_password
from api.v1.endpoints.depends.usuariodeps import get_usuario_logado

from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

router = APIRouter()

@router.get('/', response_model=List[UsuarioResponse])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario)

        result= await session.execute(query)

        usuarios: List[Usuario]= result.scalars().all()

        return usuarios

@router.get('/{usuario_id}', status_code=status.HTTP_200_OK, response_model=UsuarioResponse)
async def get_usuario(usuario_id : int , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario).filter(Usuario.id == usuario_id)
        result= await session.execute(query)
        usuario : Usuario = result.scalar_one_or_none()

        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UsuarioResponse)
async def post_usuario(usuario: Usuario, db : AsyncSession = Depends(get_session)):
    novo_usuario = Usuario(nome=usuario.nome, fone=usuario.fone, email=usuario.email, hash_password=usuario.hash_password)

    db.add(novo_usuario)
    await db.commit()

    return novo_usuario






@router.put('/{usuario_id}', status_code=status.HTTP_202_ACCEPTED, response_model=UsuarioResponse)
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
        
@router.post('/login')
async def login(usuario_email: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Usuario).filter(Usuario.email == usuario_email)
        result= await session.execute(query)
        user : Usuario = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.hash_password):
            raise HTTPException(status_code=403, 
                                detail="Email ou nome do usuário incorretos"
                                )
        return {
            "access_token": criar_token_jwt(user.id),
            "token_type": "bearer",
        }