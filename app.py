# Gerenciador de tarefas 

from fastapi import FastAPI, HTTPException
app = FastAPI()
tarefas = {}

# Adicionar tarefas com nome e descrição


# Listar tarefas
# Marcar tarefas como concluídas
# Excluir tarefas
# Menu de opções para o usuário



menu = ['Adicionar tarefa', 'Listar tarefas', 'Marcar tarefa como concluída', 'Excluir tarefa', 'Sair']
menu_formatado = '\n'.join(f'[{num}] - {opcao}' for num, opcao in enumerate(menu, start=1))
