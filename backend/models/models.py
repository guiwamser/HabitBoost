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
    dia_semana: List[DiaSemana]
    hora: str
    timer: str
    vezes: int
    check: bool = Field(default=False)
    
    usuario_id: int = Field(default=None, foreign_key="usuario.id")

    usuario: Optional[Usuario] = Relationship(back_populates="habitos")


'''
# Acima as Models..
# Abaixo os testes..

# Cria o Habito .
novoHabito = Habito(
    descricao="Correr",
    dia_semana=[DiaSemana.segunda, DiaSemana.quarta],
    hora="6:00 am",
    timer="30 min",
    vezes=3,
    check=True,
)

# Cria usuario
novoUsuario = Usuario(
    id=1,
    nome="Thiago",
    email="teste",
    hash_password="teste",
    habitos=[novoHabito]
)

# Vincula o id do usuario ao novoHabito
novoHabito.usuario_id = novoUsuario.id

## Aqui estao as impressões

# Aqui imprime o usuario inteiro
print(novoUsuario)
print()
# Aqui imprime o objeto inteiro
print(novoHabito)
print()

# Pegando apenas os habitos vinculados ao usuario 1
for usuarioHabito in novoUsuario.habitos:
    print("Descrição do Habito: " + usuarioHabito.descricao)
    for dia in usuarioHabito.dia_semana:
        print("Indice do Dia na Lista " + str(list(DiaSemana).index(dia)))
        print(dia.value)

print()
# Imprimindo apenas os dias da semana
for dia in novoHabito.dia_semana:
    print(dia.value)

print()
# Imprimindo apenas os indices dos dias (De 0 a 6)
for dia in novoHabito.dia_semana:
    print(list(DiaSemana).index(dia))
'''