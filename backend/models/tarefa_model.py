from typing import Optional
from sqlmodel import Field, SQLModel 

class TarefaModel(SQLModel, table=True):
    __tablename__: str = 'tarefas'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    data: str
    hora: str