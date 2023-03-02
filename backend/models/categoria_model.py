from typing import Optional
from sqlmodel import Field, SQLModel 

class Categoria(SQLModel, table=True):
    __tablename__: str = 'categorias'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str