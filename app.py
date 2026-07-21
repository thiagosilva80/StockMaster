from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from database.conexao import criar_conexao

app = Flask(__name__)
bcrypt = Bcrypt(app)


@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        conexao = criar_conexao()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    SELECT *
                    FROM tbl_usuario
                    WHERE email_usuario = %s
                """

                cursor.execute(sql, (email,))
                usuario = cursor.fetchone()

            if usuario and bcrypt.check_password_hash(
                usuario["senha_usuario"],
                senha
            ):
                return redirect(url_for("dashboard"))

            return "E-mail ou senha incorretos!"

        finally:
            conexao.close()

    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")

        if not nome or not email or not senha:
            return "Preencha todos os campos!"

        senha_criptografada = bcrypt.generate_password_hash(
            senha
        ).decode("utf-8")

        conexao = criar_conexao()

        try:
            with conexao.cursor() as cursor:

                # Confere se o e-mail já existe
                sql_verificar = """
                    SELECT id_usuario
                    FROM tbl_usuario
                    WHERE email_usuario = %s
                """

                cursor.execute(sql_verificar, (email,))
                usuario_existente = cursor.fetchone()

                if usuario_existente:
                    return "Este e-mail já está cadastrado!"

                # Insere o usuário
                sql_inserir = """
                    INSERT INTO tbl_usuario
                    (
                        nome_usuario,
                        email_usuario,
                        senha_usuario
                    )
                    VALUES (%s, %s, %s)
                """

                cursor.execute(
                    sql_inserir,
                    (nome, email, senha_criptografada)
                )

                conexao.commit()

            return redirect(url_for("login"))

        except Exception as erro:
            conexao.rollback()
            print("Erro ao cadastrar usuário:", erro)
            return "Erro ao cadastrar usuário."

        finally:
            conexao.close()

    return render_template("cadastro.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route ("/produtos")
def produtos():
    conexao = criar_conexao()
    
    
    try:
        with conexao.cursor() as cursor:
            sql = """
                SELECT 
                    id_produto,
                    codigo_produto,
                    nome_produto,
                    categoria_id,
                    fornecedor_id,
                    quantidade_produto,
                    preco_compra_produto,
                    preco_venda_produto,
                    data_cadastro_produto
                FROM tbl_produtos
                ORDER BY id_produto DESC
            """
            cursor.execute(sql)
            lista_produtos = cursor.fetchall()
            
        return render_template(
            "produtos.html",
            produtos=lista_produtos
        )
        
    except Exception as erro:
        print("Erro ao listar produto: ", erro)
        return "Erro ao carregar produtos."
    
    finally:
        conexao.close()
        
    
@app.route("/produtos/novos", methods =["GET", "POST"] )
def novo_produto():
    
    if request.method == "POST":
        codigo = request.form.get("codigo")
        nome = request.form.get("nome")
        categoria_id = request.form.get("categoria_id")
        fornecedor_id = request.form.get("fornecedor_id")
        quantidade = request.form.get("quantidade")
        preco_compra = request.form.get("preco_compra")
        preco_venda = request.form.get("preco_venda")
        data_cadastro = request.form.get("data_cadastro")
        
        if not codigo or not nome:
            return "Prencha o codigo e o nome do produto."
        
        conexao = criar_conexao()
        
        try:
            with conexao.cursor() as cursor: 
                sql = """
                INSERT INTP tbl_produtos(
                    codigo_produto,
                    nome_produto,
                    catagoria_id,
                    fornecedor_id,
                    quantidade_produto,
                    preco_compra_produto,
                    preco_venda_produto,
                    data_cadastro_produto
                )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    sql,
                    (
                        codigo,
                        nome, 
                        int(categoria_id),
                        int(fornecedor_id),
                        int(quantidade),
                        preco_compra.render_template(",", "."),
                        preco_venda.render_template(",", "."),
                        data_cadastro
                    )
                )
                
                conexao.commit
            
            return redirect(url_for("produtos"))
        
        except ValueError:
            conexao.rollback()
            return "Categoria, fornecedor ou quantidade inválidos."
        
        except Exception as erro:
            conexao.rollback()
            print("Erro ao cadastrar produto:", erro)
            return "Erro ao cadastrar produto."
        
        finally:
            conexao.close
            
    return render_template ("novo_produto.html")

@app.route ("/categorias")
def categorias():
    conexao = criar_conexao()
    
    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                    SELECT*
                    FROM tbl_categorias
                    ORDER BY id_categoria DESC              
            """)
            
            lista_categorias = cursor.fetchall()
          
        return render_template(
             "categorias.html",
             categorias=lista_categorias
            )

    except Exception as erro:
        print("Erro ao listar categorias", erro)
        return "Erro ao carregar categorias."
    
    finally:
        conexao.close()
        

@app.route ("/categorias/nova", methods =["GET", "POST"])
def nova_categoria():
    
    if request.method == "POST":
        nome_categoria = request.form.get("nome_categoria")
        
        if not nome_categoria:
            return "O nome da categoria é obrigatório."
        
        conexao = criar_conexao()
        
        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                INSERT INTO tbl_categorias (
                    nome_categoria
                )
                VALUES(%s)
            """, (nome_categoria,))
            
            conexao.commit()
            
            return redirect(url_for("categorias"))
    
        except Exception as erro:
            conexao.rollback()
            print("Erro ao cadastrar categoria:", erro)
            return "Erro ao cadastrar categoria."
        
        finally:
            conexao.close
    return render_template("nova_categoria.html")

@app.route("/categorias/editar/<int:id_categoria>", methods=["GET", "POST"])
def editar_categoria(id_categoria):
    conexao = criar_conexao()

    try:
        with conexao.cursor() as cursor:

            if request.method == "POST":
                nome_categoria = request.form.get("nome_categoria")

                cursor.execute("""
                    UPDATE tbl_categorias
                    SET nome_categoria = %s
                    WHERE id_categoria = %s
                """, (nome_categoria, id_categoria))

                conexao.commit()

                return redirect(url_for("categorias"))

            cursor.execute("""
                SELECT *
                FROM tbl_categorias
                WHERE id_categoria = %s
            """, (id_categoria,))

            categoria = cursor.fetchone()

        if not categoria:
            return "Categoria não encontrada.", 404

        return render_template(
            "editar_categoria.html",
            categoria=categoria
        )

    except Exception as erro:
        conexao.rollback()
        print("Erro ao editar categoria:", erro)
        return "Erro ao editar categoria."

    finally:
        conexao.close()
        
@app.route("/categorias/excluir/<int:id_categoria>")
def excluir_categoria(id_categoria):
    conexao = criar_conexao()

    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                DELETE FROM tbl_categorias
                WHERE id_categoria = %s
            """, (id_categoria,))

            conexao.commit()

        return redirect(url_for("categorias"))

    except Exception as erro:
        conexao.rollback()
        print("Erro ao excluir categoria:", erro)
        return "Erro ao excluir categoria."

    finally:
        conexao.close()
                        
if __name__ == "__main__":
    app.run(debug=True)