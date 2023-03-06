from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Usuario(SQLModel, table=True):
    __tablename__: str = 'usuarios'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    fone: str
    email: str = Field(unique=True)
    hash_password: str
    
    habito: list["habito"] = Relationship(back_populates="usuario")