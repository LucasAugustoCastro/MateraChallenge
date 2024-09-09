# Django Loan Manager API

Este projeto é uma API para gerenciar empréstimos e seus respectivos pagamentos. Os usuários podem criar, visualizar e gerenciar seus empréstimos e pagamentos de forma segura. A autenticação é feita via JWT (JSON Web Token), garantindo que apenas usuários autenticados possam acessar e gerenciar seus próprios dados.

Projeto criado para o teste [ONIDATA](https://github.com/onidata/vagas?tab=readme-ov-file)

## Funcionalidades

- **Gerenciamento de Empréstimos**: Usuários podem criar e visualizar seus empréstimos. Cada empréstimo contém informações como valor nominal, taxa de juros, cliente e banco.
- **Gerenciamento de Pagamentos**: Usuários podem adicionar pagamentos para um empréstimo e ver o saldo devedor atualizado.
- **Autenticação JWT**: A API utiliza autenticação via JSON Web Token para proteger os endpoints.
- **Cálculo de Saldo Devedor com Juros Compostos Pro Rata Dia**: O saldo devedor considera a taxa de juros e é atualizado conforme os pagamentos são feitos.

## Tecnologias Utilizadas

- **Django**: Framework principal para desenvolvimento backend.
- **Django REST Framework**: Extensão do Django para criação de APIs RESTful.
- **SimpleJWT**: Biblioteca para autenticação JWT no Django.
- **SQLite**: Banco de dados padrão para desenvolvimento local.
- **venv**: Para gerenciar o ambiente virtual e as dependências (opcional).

## Instalação

### Pré-requisitos

- **Python 3.x**: Certifique-se de que você tem o Python 3.x instalado.
- **pip**: Para instalar pacotes Python.

### Passos para Instalação

1. Clone o repositório:
    
    ```bash
    git clone https://github.com/LucasAugustoCastro/MateraChallenge.git
    cd MateraChallenge
    ```
    
2. Crie e ative o ambiente virtual:
    
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
        
3. Instale as dependências:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. Crie o banco de dados e rode as migrações:
    
    ```bash
    python manage.py migrate
    ```
    
5. Crie um superusuário (administrador)(opcional):
    ```bash
    python manage.py createsuperuser
    ```
    Ao rodar as migrations já foi criado um super user.
    - username: admin
    - password: 123456
6. Rode o servidor de desenvolvimento:
    
    ```bash
    python manage.py runserver
    ```
    

A API estará disponível em `http://127.0.0.1:8000/`.

## Endpoints Principais

### Autenticação

- **POST /api/token/**: Obtenha o token JWT.
    
    ```json
    {
      "username": "user",
      "password": "password"
    }
    
    ```
    
- **POST /api/token/refresh/**: Atualize o token JWT.

### Empréstimos

- **GET /loans/**: Lista todos os empréstimos do usuário autenticado.
- **POST /loans/**: Cria um novo empréstimo.
- **GET /loans/{id}/**: Retorna os detalhes de um empréstimo específico.
- **GET /loans/{id}/payments/**: Lista todos os pagamentos relacionados a um empréstimo.

### Pagamentos

- **GET /payments/**: Lista todos os pagamentos do usuário.
- **POST /payments/**: Cria um novo pagamento relacionado a um empréstimo.

## Exemplo de Solicitação e Resposta

### Criar um Empréstimo

- **Endpoint**: `POST /loans/`
- **Corpo da Requisição**:
    
    ```json
    {
        "nominal_value": 500000.00,
        "interest_rate": 7.94,
        "bank": "Nu bank",
        "request_date": "2024-01-01"
    }
    ```
    
- **Resposta**:
    
    ```json
    {
        "id": "7454afa4-9129-4d48-b898-72797264decb",
        "description": "",
        "nominal_value": "500000.00",
        "interest_rate": "7.94",
        "ip_address": "127.0.0.1",
        "bank": "Nu bank",
        "created_at": "2024-09-08T01:48:46.657576Z",
        "updated_at": "2024-09-08T01:48:46.657601Z",
        "deleted": false,
        "debt_balance": 539700.0,
        "payments": [],
        "request_date": "2024-01-01"
    }
    
    ```
    

### Adicionar um Pagamento

- **Endpoint**: `POST /payments/`
- **Corpo da Requisição**:
    
    ```json
    { 
        "loan": "7454afa4-9129-4d48-b898-72797264decb",
        "value": 30000,
        "payed_at": "2024-02-17"
    }
    
    ```
    
- **Resposta**:
    
    ```json
    {
        "id": "b8dc92a8-eec7-4c5c-8912-939b799d0a80",
        "loan": "7454afa4-9129-4d48-b898-72797264decb",
        "value": "30000.00",
        "payed_at": "2024-02-17T00:00:00Z",
        "created_at": "2024-09-08T01:48:43.846507Z",
        "updated_at": "2024-09-08T01:48:43.846524Z",
        "deleted": false
    }
    
    ```
    

## Rodando os Testes

Para rodar os testes automatizados:

```bash
python manage.py test
```

Certifique-se de que todos os testes estão passando antes de fazer um commit.
