from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Usuario(SQLModel, table=True):
    __tablename__: str = 'usuario'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    fone: str
    email: str = Field(unique=True)
    hash_password: str
    
    #habito: list["habito"] = Relationship(back_populates="usuario")
        
class Habito(SQLModel, table=True):
    __tablename__: str = 'habito'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    dia_semana: str
    hora: str
    timer: str
    vezes: int
    check: bool = Field(default=False)
    
    usuario_id: int = Field(default=None, foreign_key="usuario.id")
