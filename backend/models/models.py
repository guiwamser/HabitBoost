from enum import Enum
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import Session

# Ele cria o dia da semana na lista de 0 a 6
class DiaSemana(str, Enum):
    segunda = "segunda"
    terca = "terca"
    quarta = "quarta"
    quinta = "quinta"
    sexta = "sexta"
    sabado = "sabado"
    domingo = "domingo"

class Usuario(SQLModel, table=True):
    __tablename__: str = 'usuario'

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(unique=True)
    hash_password: str
    
    habitos: List["Habito"] = Relationship(back_populates="usuario")
        
class Habito(SQLModel, table=True):
    __tablename__: str = 'habito'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    dia_semana: int
    hora: str
    timer: str
    vezes: int
    check: bool = Field(default=False)
    
    usuario_id: int = Field(default=None, foreign_key="usuario.id")

    usuario: Optional[Usuario] = Relationship(back_populates="habitos")



# Acima as Models..