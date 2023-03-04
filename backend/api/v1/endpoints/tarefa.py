from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.tarefa_model import Tarefa
from core.deps import get_session
from models.requests.tarefa_create import HabitBase

from sqlmodel.sql.expression import Select, SelectOfScalar

import smtplib
from email.mime.text import MIMEText

from fastapi.middleware.cors import CORSMiddleware

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True

router = APIRouter()




@router.get('/', response_model=List[Tarefa])
async def get_tarefas(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Tarefa)

        result= await session.execute(query)

        tarefas: List[Tarefa]= result.scalars().all()

        return tarefas

@router.get('/{tarefa_id}', status_code=status.HTTP_200_OK, response_model=Tarefa)
async def get_tarefa(tarefa_id : int , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Tarefa).filter(Tarefa.id == tarefa_id)
        result= await session.execute(query)
        tarefa : Tarefa = result.scalar_one_or_none()

        if tarefa:
            return tarefa
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Tarefa)
async def post_tarefa(tarefa: Tarefa, db : AsyncSession = Depends(get_session)):
    nova_tarefa = Tarefa(descricao=tarefa.descricao, data=tarefa.data, hora=tarefa.hora, check=tarefa.check)

    db.add(nova_tarefa)
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

    return nova_tarefa



@router.put('/{tarefa_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Tarefa)
async def put_tarefa(tarefa_id : int, tarefa: Tarefa , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Tarefa).filter(Tarefa.id == tarefa_id)

        result= await session.execute(query)

        tarefa_up : Tarefa = result.scalar_one_or_none()

        if tarefa_up:
            tarefa_up.id = tarefa.id
            tarefa_up.descricao = tarefa.descricao
            tarefa_up.data = tarefa.data
            tarefa_up.hora = tarefa.hora
            tarefa_up.check = tarefa.check

            await session.commit()

            return tarefa_up
        else:
            raise HTTPException(detail='Usuário não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
@router.delete('/{tarefa_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tarefa(tarefa_id : int , db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Tarefa).filter(Tarefa.id == tarefa_id)

        result= await session.execute(query)

        tarefa_del : Tarefa = result.scalar_one_or_none()

        if tarefa_del:
            await session.delete(tarefa_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        
        else:
            raise HTTPException(detail='Tarefa não encontrada', status_code=status.HTTP_404_NOT_FOUND)