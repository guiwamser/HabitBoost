from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class Habito(SQLModel, table=True):
    __tablename__: str = 'habitos'

    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: str
    dia_semana: str
    hora: str
    check: bool = Field(default=None)
    
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")