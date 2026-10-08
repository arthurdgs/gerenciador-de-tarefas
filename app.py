

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


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
    concluida = Column(Boolean, default=False)


class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False 


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
def criar_tarefa(tarefa: Tarefa, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDb).filter(TarefaDb.nome == tarefa.nome).first()

    if db_tarefa:
        raise HTTPException(
            status_code=400, detail="Tarefa já cadastrada")

    nova_tarefa = TarefaDb(
        nome=tarefa.nome, descricao=tarefa.descricao, concluida = tarefa.concluida) 
    
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)

    return {'message': 'Tarefa criada com sucesso'}

# Listar tarefas com paginação

@app.get("/listar_tarefas/")
def listar_tarefas(ordenar_tarefas: int = 1 , page: int = 1, size: int = 10, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    if page < 1 or size < 1:
        raise HTTPException(
            status_code=400, detail="Page ou Size estão com valores inválidos")
    start = (page - 1) * size
    end = start + size

    if ordenar_tarefas == 1:
        Tarefasdb = db.query(TarefaDb).order_by(TarefaDb.nome).offset(start).limit(size).all()
    elif ordenar_tarefas == 2:
        Tarefasdb = db.query(TarefaDb).order_by(TarefaDb.descricao).offset(start).limit(size).all()
    elif ordenar_tarefas == 3:
        Tarefasdb = db.query(TarefaDb).order_by(TarefaDb.concluida).offset(start).limit(size).all()


    total_tarefas = db.query(TarefaDb).count()
    
    if not Tarefasdb:
        return {'message': 'Nenhuma tarefa encontrada'}

    return {
        'page': page,
        'size': size,
        'total': total_tarefas,
        'tarefas': [{'tarefa': tarefa.nome, 'descricao': tarefa.descricao, 'concluida': tarefa.concluida} for tarefa in Tarefasdb]
    }


# Marcar tarefas como concluídas

@app.put("/concluir_tarefa/{nome}")
def concluir_tarefa(nome: str, db: Session = Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    db_tarefa = db.query(TarefaDb).filter(TarefaDb.nome == nome).first()

    if not db_tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db_tarefa.concluida = True
    db.commit()
    db.refresh(db_tarefa)
    return {'message': 'Tarefa marcada como concluída'}

# Excluir tarefas

@app.delete("/excluir_tarefa/{nome}")
def excluir_tarefa(nome: str, db: Session =Depends(sessao_db), credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
    # 1. Verifica se a lista está vazia

   db_tarefa = db.query(TarefaDb).filter(TarefaDb.nome == nome).first()

   if not db_tarefa:
       raise HTTPException(status_code=404, detail="Tarefa não encontrada")

   db.delete(db_tarefa)
   db.commit()
    
   return {'message': 'Tarefa excluída com sucesso'}