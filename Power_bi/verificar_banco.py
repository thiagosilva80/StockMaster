
import sqlite3
from pathlib import Path

# Localiza o banco exclusivo do Power BI
BASE_DIR = Path(__file__).resolve().parent
CAMINHO_BANCO = BASE_DIR / "stockmaster_bi.db"

# Verifica se o arquivo existe
if not CAMINHO_BANCO.exists():
    print("Banco do Power BI não encontrado!")
    raise SystemExit

conexao = sqlite3.connect(CAMINHO_BANCO)
cursor = conexao.cursor()

tabelas = [
    "tbl_categorias",
    "tbl_fornecedores",
    "tbl_produtos",
    "tbl_movimentacoes"
]

for tabela in tabelas:
    print(f"\n--- {tabela} ---")

    cursor.execute(f"PRAGMA table_info({tabela})")

    colunas = cursor.fetchall()

    if not colunas:
        print("Tabela não encontrada!")
        continue

    for coluna in colunas:
        print(f"{coluna[1]} - {coluna[2]}")

    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    print("Total de registros:", cursor.fetchone()[0])

conexao.close()
