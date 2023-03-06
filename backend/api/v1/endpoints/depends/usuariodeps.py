from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, ValidationError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.deps import get_session

from models.models import Usuario
from core.security import SECRET_KEY, JWT_ALGORITHM


class TokenPayload(BaseModel):
    sub: Optional[int] = None

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/usuarios/login"
)

async def get_usuario_logado(
    token: str = Depends(reusable_oauth2), db: AsyncSession = Depends(get_session)
) -> Usuario:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não conseguimos validar suas credenciais",
        )
    async with db as session:
        query = select(Usuario).filter(Usuario == token_data.sub)
        result= await session.execute(query)
        user : Usuario = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user
