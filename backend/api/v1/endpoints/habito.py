from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.models import Habito
from core.deps import get_session
from models.requests.tarefa_create import HabitBase

from sqlmodel.sql.expression import Select, SelectOfScalar

import smtplib
from email.mime.text import MIMEText

from fastapi.middleware.cors import CORSMiddleware

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

router = APIRouter()

@router.get('/', response_model=List[Habito])
async def get_habitos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Habito)

        result= await session.execute(query)

        habitos: List[Habito]= result.scalars().all()

        return habitos

@router.get('/{habito_id}', status_code=status.HTTP_200_OK, response_model=Habito)
async def get_habito(habito_id : int , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Habito).filter(Habito.id == habito_id)
        result= await session.execute(query)
        habito : Habito = result.scalar_one_or_none()

        if habito:
            return habito
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Habito)
async def post_habito(habito: Habito, db : AsyncSession = Depends(get_session)):
    novo_habito = Habito(descricao=habito.descricao, dia_semana=habito.dia_semana, hora=habito.hora, check=habito.check, usuario_id=habito.usuario_id)

    db.add(novo_habito)
    await db.commit()

    """""
    try:
            sender = "habitboostpy@gmail.com"
            recipient = "vanderlaus@hotmail.com"
            subject = "New task created"
            body = "A new task has been created with the following details:\n\n"

            message = MIMEText(body)
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = recipient

            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "habitboostpy@gmail.com"
            smtp_password = "HabitBoost!py"

            smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
            smtp_connection.starttls()
            smtp_connection.login(smtp_username, smtp_password)
            smtp_connection.sendmail(sender, [recipient], message.as_string())
            smtp_connection.quit()

    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send notification email")

    return {"message": "Task created successfully"}"""

    return novo_habito



@router.put('/{habito_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Habito)
async def put_habito(habito_id : int, habito: Habito , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Habito).filter(Habito.id == habito_id)

        result= await session.execute(query)

        habito_up : Habito = result.scalar_one_or_none()

        if habito_up:
            habito_up.id = habito.id
            habito_up.descricao = habito.descricao
            habito_up.dia_semana = habito.dia_semana
            habito_up.hora = habito.hora
            habito_up.check = habito.check

            await session.commit()

            return habito_up
        else:
            raise HTTPException(detail='Habito não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
@router.delete('/{habito_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_habito(habito_id : int , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Habito).filter(Habito.id == habito_id)

        result= await session.execute(query)

        habito_del : Habito = result.scalar_one_or_none()

        if habito_del:
            await session.delete(habito_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Habito não encontrado', status_code=status.HTTP_404_NOT_FOUND)