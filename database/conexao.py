import pymysql

def criar_conexao():
    conexao = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_estoque",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )

    return conexao
