from fastapi import FastAPI, HTTPException
app = FastAPI()
lista_tarefas = {}

# Adicionar tarefas

@app.post("/criar_tarefa/")
def criar_tarefa(id_tarefa: int,nome_tarefa: str, descricao_tarefa: str, concluida: bool = False):
   if id_tarefa in lista_tarefas:
       raise HTTPException(status_code=400, detail="Tarefa já existe")
   else:
       lista_tarefas[id_tarefa] = {'nome_tarefa': nome_tarefa, 'Descrição': descricao_tarefa, 'Concluída': concluida}
       return {'message': 'Tarefa criada com sucesso'}
   
# Listar tarefas

@app.get("/listar_tarefas/")
def listar_tarefas():
    if not lista_tarefas:
        return {'message': 'Nenhuma tarefa encontrada'}
    for tarefa,dados in lista_tarefas.items():
        return f'\n'.join(f'id: {tarefa} - Tarefa: {dados['nome_tarefa']} - Descrição: {dados['Descrição']} - Concluída: {dados['Concluída']}' for tarefa, dados in lista_tarefas.items()) 
    
# Marcar tarefas como concluídas

@app.put("/concluir_tarefa/{id_tarefa}")
def concluir_tarefa(id_tarefa:int):
    if id_tarefa not in lista_tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        lista_tarefas[id_tarefa]['Concluída'] = True
        return {'message': f'Tarefa {id_tarefa} marcada como concluída'}
    
# Excluir tarefas

@app.delete("/excluir_tarefa/{id_tarefa}")
def excluir_tarefa(id_tarefa: int):
    if id_tarefa not in lista_tarefas:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    else:
        del lista_tarefas[id_tarefa]
        return {'message': f'Tarefa {id_tarefa} excluída com sucesso'}