from typing import Optional
from sqlmodel import Field, SQLModel 
from datetime import date, time, datetime

class Tarefa(SQLModel, table=True):
    __tablename__: str = 'tarefas'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    data: date
    hora: time
    check: bool = Field(default=None)
    