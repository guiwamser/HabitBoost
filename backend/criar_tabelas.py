from sqlmodel import SQLModel
from core.database import engine

from models.categoria_model import CategoriaModel
from models.tarefa_model import TarefaModel
from models.user_model import UserModel

print('executando documento')
async def create_tables() -> None:
    print('executando funcao')

    
    print('Criando tabela no banco de dados')

    async with engine.begin() as conn:

        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    print('Tabela criada com sucesso')

if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())