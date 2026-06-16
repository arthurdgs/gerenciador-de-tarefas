from fastapi import FastAPI, HTTPException, Depends 
import json 
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets 
import os 

# Autenticação de usuário 

MEU_USUÁRIO = 'admin'
MINHA_SENHA = 'admin'

security = HTTPBasic()

def autenticar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUÁRIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"}
        )

app = FastAPI()
lista_tarefas = []

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

# Adicionar tarefas
 #Ao invés de adicionar as tarefas em um dicionário, deve adicionar um objeto do tipo tarefa

@app.post("/criar_tarefa/")
def criar_tarefa(tarefa: Tarefa, credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
   for t in lista_tarefas:
       if t.nome == tarefa.nome:
           raise HTTPException(status_code=400, detail="Tarefa já existe")

   lista_tarefas.append(tarefa)
   return {'message': 'Tarefa criada com sucesso'}


# Listar tarefas com paginação

@app.get("/listar_tarefas/")
def listar_tarefas():
    if not lista_tarefas:
        return {'message': 'Nenhuma tarefa encontrada'}
    else:
        lista_tarefas_json = [t.model_dump() for t in lista_tarefas]
        return {'tarefas': lista_tarefas_json}

        
       

# Marcar tarefas como concluídas

@app.put("/concluir_tarefa/{nome}")
def concluir_tarefa(nome: str,credentials: HTTPBasicCredentials = Depends(autenticar_usuario)):
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
        raise HTTPException(status_code=404, detail="Não há tarefas cadastradas")

    # 2. Procura a tarefa pelo nome e remove se encontrar
    for t in lista_tarefas:
        if t.nome == nome:
            lista_tarefas.remove(t)
            return {'message': 'Tarefa excluída com sucesso'}
    
    # 3. Se o loop rodar inteiro e não achar/retornar nada, a tarefa não existe
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")