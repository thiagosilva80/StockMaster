# 📦 StockMaster

Sistema web de controle de estoque desenvolvido com **Flask** e **MySQL**, com autenticação de usuários, cadastro de produtos, controle de entradas/saídas e relatórios em dashboard.

## ✨ Funcionalidades

- 🔐 Autenticação de usuários (cadastro/login com senha criptografada via bcrypt)
- 📋 CRUD completo de produtos (criar, listar, editar, excluir)
- 🔄 Registro de movimentações de estoque (entrada e saída)
- 📊 Dashboard com indicadores em tempo real (valor em estoque, produtos com estoque baixo, movimentações recentes)
- 📈 Relatórios (valor por categoria, total de entradas/saídas, alertas de estoque baixo)

## 🛠️ Tecnologias

- Python / Flask
- Flask-SQLAlchemy (ORM)
- Flask-Login (sessão de usuário)
- Flask-Bcrypt (hash de senhas)
- MySQL (PyMySQL)
- HTML / CSS / JS

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/stockmaster.git
cd stockmaster
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Crie um banco MySQL chamado `sistema_estoque` (ou use o script em `database/schema.sql`).

### 5. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o `.env` com seu usuário e senha do MySQL.

### 6. Execute a aplicação

```bash
python app.py
```

Acesse em [http://localhost:5000](http://localhost:5000)

## 📁 Estrutura do projeto

```
StockMaster/
├── app.py                  # Rotas e lógica principal
├── config.py                # Configurações (via variáveis de ambiente)
├── database/
│   └── schema.sql           # Script SQL de referência
├── models/
│   ├── usuario.py
│   ├── produto.py
│   └── movimentacao.py
├── static/
│   ├── css/
│   └── js/
├── templates/
└── requirements.txt
```

## 📄 Licença

Este projeto está sob a licença MIT.
