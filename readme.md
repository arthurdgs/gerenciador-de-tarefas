# API de Lista de Tarefas 📝

Esta API tem como objetivo fornecer o back-end para um gerenciador de tarefas, permitindo que o usuário adicione, remova e edite o status das tarefas.

## 🚀 Tecnologias Utilizadas

* **Python**
* **FastAPI**
* **Poetry**
* **Docker / Podman**
* **Docker Compose / Podman Compose**

## 📋 Pré-requisitos

Para rodar o projeto, você precisará da seguinte ferramenta instalada em sua máquina:

* [Podman](https://podman.io/) 

## 🔧 Passo a Passo para Execução

**1. Clone o repositório**
Abra o seu terminal e execute o comando abaixo para baixar o código fonte:
```bash
git clone <https://github.com/arthurdgs/backend-ebac-livros.git>


**2. Crie a imagem e inicie o container**
Execute o comando abaixo:
    "podman-compose up --build -d"

**3. Acessando a API**
Após inicializar o container, a API estará disponível localmente. Você pode acessar a documentação pelo navegador 
Obs: Caso a porta mapeada seja a 8000
   url: http://localhost:8000/docs


**4. Para derrubar a aplicação**
Execute o comando abaixo: 

    "podman-compose down" 