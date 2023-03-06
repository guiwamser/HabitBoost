from pydantic import BaseModel


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    fone: str
    email: str