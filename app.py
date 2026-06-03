''' Gerenciador de tarefas para usuários utilizando FastAPI.
1 - Criação de usuários: Permitir que os usuários se registrem fornecendo um ID, nome, idade e email.
2 - Criação de tarefas: Permitir que os usuários criem tarefas associadas a eles, fornecendo um ID de tarefa, nome da tarefa, descrição e status de conclusão.
3 - Listagem de tarefas: Permitir que os usuários visualizem suas tarefas, incluindo detalhes como nome da tarefa, descrição e status de conclusão.
4 - Atualização de tarefas: Permitir que os usuários atualizem o status de conclusão de suas tarefas.
5 - Exclusão de tarefas: Permitir que os usuários excluam tarefas específicas.

'''

from fastapi import FastAPI, HTTPException

app = FastAPI()
usuarios = {}
lista_tarefas = {}

def criar_usuario(id_usuario, nome, idade, email):
    if id_usuario in usuarios:
        raise HTTPException(status_code=400, detail="ID de usuário já existe.")
    else:
        nome = usuario(id_usuario, nome, idade, email)
        usuarios[id_usuario] = {'nome': nome, 'idade': idade, 'email': email}
        return f"Usuário {nome} criado com sucesso."

class usuario:
    def __init__(self,id_usuario,nome,idade,email):
        self.id_usuario = id_usuario
        self.nome = nome
        self.idade = idade
        self.email = email
     
    def exibir_dados(self):
        print(f"Nome: {self.nome}")
        print(f"Idade: {self.idade}")
        print(f"Email: {self.email}")
    
    
class tarefas:
    def __init__(self,id_tarefa,nome_tarefa,descricao_tarefa,concluida,id_usuario):
        self.id_tarefa = id_tarefa
        self.nome_tarefa = nome_tarefa
        self.descricao_tarefa = descricao_tarefa
        self.concluida = False
        self.id_usuario = id_usuario
    
        def criar_tarefa(self):
            if id_tarefa in lista_tarefas:
                raise HTTPException(status_code=400, detail="ID de tarefa já existe.")
            else:
                nome_tarefa = tarefas(id_tarefa, nome_tarefa, descricao_tarefa, concluida, id_usuario)
                lista_tarefas[id_tarefa] = {'nome_tarefa': nome_tarefa, 'descricao_tarefa': descricao_tarefa, 'concluida': concluida, 'id_usuario': id_usuario}
                return f"Tarefa {nome_tarefa} criada com sucesso para o usuário {usuarios[id_usuario]['nome']}."


__name_-_ = "__main__"