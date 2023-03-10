from typing import Optional
from sqlmodel import Field, SQLModel 

class CategoriaModel(SQLModel, table=True):
    __tablename__: str = 'categorias'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str