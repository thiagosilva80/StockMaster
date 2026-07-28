from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from database.conexao import criar_conexao

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "stockmaster-chave-secreta"


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
                session["usuario_id"] = usuario["id_usuario"]
                session["usuario_nome"] = usuario["nome_usuario"]
                session["usuario_email"] = usuario["email_usuario"]

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

            
                sql_verificar = """
                    SELECT id_usuario
                    FROM tbl_usuario
                    WHERE email_usuario = %s
                """

                cursor.execute(sql_verificar, (email,))
                usuario_existente = cursor.fetchone()

                if usuario_existente:
                    return "Este e-mail já está cadastrado!"

        
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
        
    
@app.route("/produtos/novos", methods=["GET", "POST"])
def novo_produto():

    conexao = criar_conexao()

    try:
        with conexao.cursor() as cursor:

           
            cursor.execute("""
                SELECT
                    id_categoria,
                    nome_categoria
                FROM tbl_categorias
                ORDER BY nome_categoria
            """)

            categorias = cursor.fetchall()

            cursor.execute("""
                SELECT
                    id_fornecedores,
                    nome_fornecedores
                FROM tbl_fornecedores
                ORDER BY nome_fornecedores
            """)

            fornecedores = cursor.fetchall()

        

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
                return "Preencha o código e o nome do produto."

            with conexao.cursor() as cursor:

                sql = """
                    INSERT INTO tbl_produtos (
                        codigo_produto,
                        nome_produto,
                        categoria_id,
                        fornecedor_id,
                        quantidade_produto,
                        preco_compra_produto,
                        preco_venda_produto,
                        data_cadastro_produto
                    )

                    VALUES (
                        %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                """

                valores = (
                    codigo,
                    nome,
                    int(categoria_id),
                    int(fornecedor_id),
                    int(quantidade),
                    float(preco_compra.replace(",", ".")),
                    float(preco_venda.replace(",", ".")),
                    data_cadastro
                )

                cursor.execute(sql, valores)

                conexao.commit()

            return redirect(url_for("produtos"))

        return render_template(
            "novo_produto.html",
            categorias=categorias,
            fornecedores=fornecedores
        )

    except ValueError:

        conexao.rollback()

        return "Quantidade ou preço inválido."

    except Exception as erro:

        conexao.rollback()

        print("Erro ao cadastrar produto:", erro)

        return "Erro ao cadastrar produto."

    finally:

        conexao.close()

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
            conexao.close()
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
        
@app.route("/entradas", methods=["GET", "POST"])
def entrada():
    conexao = criar_conexao()
    
    try:
        if request.method == "POST":
            produtos_id = request.form.get("produto_id")
            quantidade = request.form.get("quantidade")
            
            if not produtos_id or not quantidade:
                return "Selecione o produto e informe a quantidade."
            
            produtos_id = int(produtos_id)
            quantidade = int(quantidade)
            
            if quantidade <= 0:
                return "A quantidade deve ser maior que zero."
            
            with conexao.cursor() as cursor:
                
                cursor.execute("""
                UPDATE tbl_produtos
                SET quantidade_produto =
                    quantidade_produto + %s
                WHERE id_produto = %s               
            """, (
                quantidade,
                produtos_id
            ))
                
                cursor.execute("""
                INSERT INTO tbl_movimentacoes(
                    produtos_id,
                    tipo_movimentacoes,
                    quantidade_movimentacoes,
                    data_movimentacoes              
                    )
                    VALUES(%s, %s, %s, NOW())
                    """, (
                        produtos_id,
                        "Entrada",
                        quantidade
                    ))
                    
                conexao.commit()
                
            return redirect(url_for("entrada"))
        
        with conexao.cursor() as cursor:
            
            cursor.execute("""
                SELECT 
                id_produto,
                nome_produto
            FROM tbl_produtos
            ORDER BY nome_produto           
        """)
            produtos = cursor.fetchall()
            
        return render_template(
            "entrada.html",
            produtos=produtos
        )
        
    except Exception as erro:
        conexao.rollback()
        
        print("Erro na entrada:", erro)
        
        return "Erro ao registrar entrada."
    
    finally:
        conexao.close()
        

@app.route("/saidas", methods=["GET", "POST"])

def saida():
    conexao = criar_conexao()
    
    try:
        
        if request.method == "POST":
            
            produto_id = request.form.get("produto_id")
            quantidade = request.form.get("quantidade")
            
            if not produto_id or not quantidade:
                return "Selecione o produto e informe a quantidade."
            
            produto_id = int(produto_id)
            quantidade = int(quantidade)
            
            if quantidade <= 0:
                return"A quantidade deve ser maior que zero."
            
            with conexao.cursor() as cursor:
                
                cursor.execute ("""
                SELECT
                    nome_produto,
                    quantidade_produto
                FROM tbl_produtos
                WHERE id_produto = %s
                """, (produto_id,))

                produto = cursor.fetchone()
                
                if not produto:
                    return "Prodouto não encontrado."
                
                estoque_atual = produto["quantidade_produto"]
                
                
                if quantidade > estoque_atual:
                    return(
                        f"Estoque insuficiente."
                        f"Quantidade disponivel: {estoque_atual}."
                    )
                    
                cursor.execute("""
                    UPDATE tbl_produtos
                    SET quantidade_produto =
                        quantidade_produto - %s
                    WHERE id_produto = %s            
                """, (
                    quantidade,
                    produto_id
                ))
                
                cursor.execute("""
                INSERT INTO tbl_movimentacoes (
                    produtos_id,
                    tipo_movimentacoes,
                    quantidade_movimentacoes,
                    data_movimentacoes
                )
                VALUES (%s, %s, %s, NOW())
                """, (
                    produto_id,
                    "Saída",
                    quantidade
                ))
                
                conexao.commit()
            
            return redirect(url_for("saida"))
        
        with conexao.cursor() as cursor:
            
            cursor.execute("""
                SELECT
                    id_produto,
                    nome_produto,
                    quantidade_produto
                FROM tbl_produtos
                ORDER BY nome_produto             
            """)
            
            produtos = cursor.fetchall()
            
            return render_template(
                "saida.html",
                produtos=produtos
            )
            
    except ValueError:
        
        conexao.rollback()
        
        return "Produto ou quantidade inválidos."
    
    except Exception as erro:
        
        conexao.rollback()
        
        print("Erro na saida:", erro)
        
        return "Erro ao registrar saida."
    
    finally:
        conexao.close()
        
@app.route("/historico")
def historico():
    conexao = criar_conexao()

    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                SELECT
                    m.id_movimentacoes AS id_movimentacao,
                    p.nome_produto AS nome_produto,
                    m.tipo_movimentacoes AS tipo_movimentacao,
                    m.quantidade_movimentacoes AS quantidade_movimentacao,
                    m.data_movimentacoes AS data_movimentacao
                FROM tbl_movimentacoes AS m

                INNER JOIN tbl_produtos AS p
                    ON m.produtos_id = p.id_produto

                ORDER BY m.data_movimentacoes DESC
            """)

            movimentacoes = cursor.fetchall()

        return render_template(
            "historico.html",
            movimentacoes=movimentacoes
        )

    except Exception as erro:
        print("Erro ao carregar histórico:", erro)
        return "Erro ao carregar histórico."

    finally:
        conexao.close()
        
@app.route("/relatorios")
def relatorios():
    conexao = criar_conexao()

    try:
        with conexao.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*) AS total_produtos
                FROM tbl_produtos
            """)
            total_produtos = cursor.fetchone()["total_produtos"]

            cursor.execute("""
                SELECT COUNT(*) AS estoque_baixo
                FROM tbl_produtos
                WHERE quantidade_produto <= 5
            """)
            estoque_baixo = cursor.fetchone()["estoque_baixo"]

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(quantidade_movimentacoes),
                        0
                    ) AS total_entradas
                FROM tbl_movimentacoes
                WHERE tipo_movimentacoes = 'Entrada'
            """)
            total_entradas = cursor.fetchone()["total_entradas"]

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(quantidade_movimentacoes),
                        0
                    ) AS total_saidas
                FROM tbl_movimentacoes
                WHERE tipo_movimentacoes = 'Saída'
            """)
            total_saidas = cursor.fetchone()["total_saidas"]

            cursor.execute("""
                SELECT
                    p.nome_produto,
                    p.quantidade_produto
                FROM tbl_produtos AS p
                ORDER BY p.quantidade_produto ASC
                LIMIT 5
            """)
            produtos_criticos = cursor.fetchall()

        return render_template(
            "relatorios.html",
            total_produtos=total_produtos,
            estoque_baixo=estoque_baixo,
            total_entradas=total_entradas,
            total_saidas=total_saidas,
            produtos_criticos=produtos_criticos
        )

    except Exception as erro:
        print("Erro ao carregar relatórios:", erro)
        return "Erro ao carregar relatórios."

    finally:
        conexao.close()
        

@app.route("/configuracoes")
def configuracoes():

    usuario = {
        "nome": session.get("usuario_nome", "Usuário"),
        "email": session.get("usuario_email", "E-mail não informado")
    }

    return render_template(
        "configuracoes.html",
        usuario=usuario,
        versao="1.0.0"
    )
    
@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)