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
