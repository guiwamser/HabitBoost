from pydantic import BaseModel, validator
from typing import Optional
from datetime import date


class HabitBase(BaseModel):
    id: int
    descricao: str
    data: date
    hora: int
    check: bool

    @validator('descricao')
    def descricao_not_empty(cls, v):
        if not v:
            raise ValueError('Nome nao pode ser vazio')
        return v

    @validator('hora')
    def hora_not_negative(cls, v):
        if v < 0:
            raise ValueError('hora nao pode ser negativa')
        return v
