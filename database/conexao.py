import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = BASE_DIR / "stockmaster.db"


class CursorSQLite:
    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, tipo_erro, valor_erro, traceback):
        self.cursor.close()

    def execute(self, sql, parametros=()):
        # Converte comandos do MySQL para SQLite.
        sql = sql.replace("%s", "?")
        sql = sql.replace("NOW()", "CURRENT_TIMESTAMP")

        return self.cursor.execute(sql, parametros)

    def fetchone(self):
        resultado = self.cursor.fetchone()

        if resultado is None:
            return None

        return dict(resultado)

    def fetchall(self):
        return [dict(linha) for linha in self.cursor.fetchall()]

    @property
    def rowcount(self):
        return self.cursor.rowcount

    @property
    def lastrowid(self):
        return self.cursor.lastrowid


class ConexaoSQLite:
    def __init__(self, caminho):
        self.conexao = sqlite3.connect(
            caminho,
            check_same_thread=False
        )

        self.conexao.row_factory = sqlite3.Row
        self.conexao.execute("PRAGMA foreign_keys = ON")

    def cursor(self):
        return CursorSQLite(self.conexao.cursor())

    def commit(self):
        self.conexao.commit()

    def rollback(self):
        self.conexao.rollback()

    def close(self):
        self.conexao.close()


def criar_tabelas(conexao):
    comandos = [
        """
        CREATE TABLE IF NOT EXISTS tbl_usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL,
            email_usuario TEXT NOT NULL UNIQUE,
            senha_usuario TEXT NOT NULL
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS tbl_categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_categoria TEXT NOT NULL
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS tbl_fornecedores (
            id_fornecedores INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_fornecedores TEXT NOT NULL,
            telefone_fornecedores TEXT,
            email_fornecedores TEXT,
            cnpj_fornecedores TEXT UNIQUE,
            endereco TEXT
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS tbl_produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_produto TEXT NOT NULL,
            nome_produto TEXT NOT NULL,
            categoria_id INTEGER,
            fornecedor_id INTEGER,
            quantidade_produto INTEGER DEFAULT 0,
            preco_compra_produto REAL DEFAULT 0,
            preco_venda_produto REAL DEFAULT 0,
            data_cadastro_produto TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (categoria_id)
                REFERENCES tbl_categorias(id_categoria),

            FOREIGN KEY (fornecedor_id)
                REFERENCES tbl_fornecedores(id_fornecedores)
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS tbl_movimentacoes (
            id_movimentacoes INTEGER PRIMARY KEY AUTOINCREMENT,
            produtos_id INTEGER NOT NULL,
            tipo_movimentacoes TEXT NOT NULL,
            quantidade_movimentacoes INTEGER NOT NULL,
            data_movimentacoes TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (produtos_id)
                REFERENCES tbl_produtos(id_produto)
        )
        """
    ]

    cursor = conexao.conexao.cursor()

    try:
        for comando in comandos:
            cursor.execute(comando)

        conexao.commit()

    finally:
        cursor.close()


def criar_conexao():
    conexao = ConexaoSQLite(CAMINHO_BANCO)
    criar_tabelas(conexao)

    return conexao