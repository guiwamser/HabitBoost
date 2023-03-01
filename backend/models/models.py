from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    __tablename__: str = 'user'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    fone: int
    email: int
    senha: str
    
    tarefa: list["tarefa"] = Relationship(back_populates="user")

class Categoria(SQLModel, table=True):
    __tablename__: str = 'categoria'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str

    tarefa: list["tarefa"] = Relationship(back_populates="categoria")
        
class Tarefa(SQLModel, table=True):
    __tablename__: str = 'tarefa'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    data: str
    hora: str
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
