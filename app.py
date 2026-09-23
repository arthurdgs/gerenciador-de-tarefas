

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "sqlite:///./tarefas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()





# Autenticação de usuário

MEU_USUÁRIO = 'admin'
MINHA_SENHA = 'admin'

security = HTTPBasic()


def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(
        credentials.username, MEU_USUÁRIO)
    is_password_correct = secrets.compare_digest(
        credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"}
        )





app = FastAPI()
lista_tarefas = []


class TarefaDb(Base):
   __tablename__ = "tarefas"
   id = Column(Integer, primary_key=True, index=True)
   nome = Column(String, unique=True, index=True)
   descricao = Column(String)
   concluida = Column(String) 

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool

Base.metadata.create_all(bind=engine)

def sessao_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Adicionar tarefas
 # Ao invés de adicionar as tarefas em um dicionário, deve adicionar um objeto do tipo tarefa


@app.post("/criar_tarefa/")
def criar_tarefa(tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    for t in lista_tarefas:
        if t.nome == tarefa.nome:
            raise HTTPException(status_code=400, detail="Tarefa já existe")

    lista_tarefas.append(tarefa)
    return {'message': 'Tarefa criada com sucesso'}


# Listar tarefas com paginação

@app.get("/listar_tarefas/")
def listar_tarefas(ordenar_tarefas: str = 'descricao', page: int = 1, size: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=400, detail="Page ou Size estão com valores inválidos")
    start = (page - 1) * size
    end = start + size

    if not lista_tarefas:
        return {'message': 'Nenhuma tarefa encontrada'}
    else:
        lista_tarefas_json = [t.model_dump() for t in lista_tarefas]

        # Lógica da ordenação (nome,descrição ou status)

        if ordenar_tarefas == 'nome':
            lista_tarefas_json = sorted(
                lista_tarefas_json, key=lambda x: x.get('nome'))

        elif ordenar_tarefas == 'descricao':
            lista_tarefas_json = sorted(
                lista_tarefas_json, key=lambda x: x.get('descricao'))

        elif ordenar_tarefas == 'concluida':
            lista_tarefas_json = sorted(
                lista_tarefas_json, key=lambda x: x.get('concluida')) 
            
         # Caso não seja nenhum dos parâmetro válidos, retorna um erro 400   
        else:
            raise HTTPException(
                status_code=400, detail="Parâmetro de ordenação inválido")

    return {
        'page': page,
        'size': size,
        'total': len(lista_tarefas_json),
        'tarefas': lista_tarefas_json[start:end],
    }


# Marcar tarefas como concluídas

@app.put("/concluir_tarefa/{nome}")
def concluir_tarefa(nome: str, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if not lista_tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        for tarefa in lista_tarefas:
            if tarefa.nome == nome:
                tarefa.concluida = True
    return {'message': 'Tarefa marcada como concluída'}


# Excluir tarefas

@app.delete("/excluir_tarefa/{nome}")
def excluir_tarefa(nome: str, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    # 1. Verifica se a lista está vazia
    if not lista_tarefas:
        raise HTTPException(
            status_code=404, detail="Não há tarefas cadastradas")

    # 2. Procura a tarefa pelo nome e remove se encontrar
    for t in lista_tarefas:
        if t.nome == nome:
            lista_tarefas.remove(t)
            return {'message': 'Tarefa excluída com sucesso'}

    # 3. Se o loop rodar inteiro e não achar/retornar nada, a tarefa não existe
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
