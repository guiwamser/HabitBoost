from typing import Optional
from sqlmodel import Field, SQLModel 

class Usuario(SQLModel, table=True):
    __tablename__: str = 'usuarios'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    fone: int
    email: str
    senha: str