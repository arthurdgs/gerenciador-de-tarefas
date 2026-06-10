from fastapi import FastAPI, HTTPException
import json 
from pydantic import BaseModel, Field

app = FastAPI()
lista_tarefas = []

class Tarefa(BaseModel):
    nome: str
    descricao: str
    concluida: bool = False

# Adicionar tarefas
 #Ao invés de adicionar as tarefas em um dicionário, deve adicionar um objeto do tipo tarefa'''

@app.post("/criar_tarefa/")
def criar_tarefa(tarefa: Tarefa):
   for t in lista_tarefas:
       if t.nome == tarefa.nome:
           raise HTTPException(status_code=400, detail="Tarefa já existe")

   lista_tarefas.append(tarefa)
   return {'message': 'Tarefa criada com sucesso'}


# Listar tarefas

@app.get("/listar_tarefas/")
def listar_tarefas():
    if not lista_tarefas:
        return {'message': 'Nenhuma tarefa encontrada'}
    else:
        lista_tarefas_json = [t.model_dump() for t in lista_tarefas]
        return {'tarefas': lista_tarefas_json}

# Marcar tarefas como concluídas

@app.put("/concluir_tarefa/{nome}")
def concluir_tarefa(nome: str):
    if not lista_tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        for tarefa in lista_tarefas:
            if tarefa.nome == nome:
                tarefa.concluida = True
            return {'message': 'Tarefa marcada como concluída'}
        
    
# Excluir tarefas

@app.delete("/excluir_tarefa/{nome}")
def excluir_tarefa(nome: str):
    if not lista_tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        for t in lista_tarefas:
            if t.nome == nome:
                lista_tarefas.remove(t)
                return {'message': 'Tarefa excluída com sucesso'}