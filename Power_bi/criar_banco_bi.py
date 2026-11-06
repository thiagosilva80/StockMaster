
import sqlite3
from pathlib import Path

# Localiza a pasta principal do StockMaster
BASE_DIR = Path(__file__).resolve().parent.parent

# Banco original
banco_original = BASE_DIR / "stockmaster.db"

# Banco exclusivo para o Power BI
banco_bi = BASE_DIR / "power_bi" / "stockmaster_bi.db"

# Verifica se o banco original existe
if not banco_original.exists():
    print("Erro: banco original não encontrado.")

elif banco_bi.exists():
    print("O banco do Power BI já existe. Nenhum arquivo foi alterado.")

else:
    # Cria uma cópia consistente do banco SQLite
    with sqlite3.connect(banco_original) as origem:
        with sqlite3.connect(banco_bi) as destino:
            origem.backup(destino)

    print("Banco StockMaster BI criado com sucesso!")
    print(f"Localização: {banco_bi}")
