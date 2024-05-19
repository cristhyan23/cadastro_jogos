
from flask import render_template,request,redirect,session,flash,url_for
from bd.jogo import Jogo
from bd.listador_jogos import ListadorJogos
from bd.usuario import Usuario
from functools import wraps
from jogoteca import app

user = Usuario()

#Função para extrair lista de jogos por usuário atualizada
def lista_de_jogos():
    jogos = ListadorJogos() #busca todos os jogos são no BD
    return jogos.select_jogos(session['usuario_logado'])

#FUNÇÃO PARA GARANTIR QUE SÓ PODE EXECUTAR SE ESTIVER LOGADO
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_logado' not in session or session['usuario_logado'] == None:
            flash('Você precisa estar logado para acessar esta página.')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

#lista de jogos
@app.route("/lista_jogos")
@login_required
def lista_jogos():
    LISTA_JOGOS = lista_de_jogos()
     # devolve a lista de objeto jogo
    return render_template("lista.html", titulo = 'Jogos', jogos=LISTA_JOGOS,enumerate=enumerate) #mostra pagina html

#ROTA DIRECIONA PARA PAGINA CADASTRO
@app.route("/ir_cadastro", methods=['GET',])
def ir_cadastro():
    return redirect(url_for('cadastro'))

#ROTA PAGINA CADASTRO
@app.route("/cadastro")
@login_required
def cadastro():
    return render_template("cadastro_jogos.html", titulo = 'Cadastro Jogos') #mostra pagina html

#ROTA PRA CRIAR JOGOS
@app.route("/criar", methods=['POST',])
@login_required
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console,session['usuario_logado'])
    msg = jogo.salvar_jogo_bd() #salva jogo na base de dados
    flash(msg)
    return redirect(url_for("lista_jogos")) 

#PAGINA LOGIN
@app.route("/")
def login():
    return render_template("login.html")

#ROTA PARA LOGIN
@app.route("/autenticar", methods=['POST',])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario == '' or senha == '':
        flash("Adicionar dados do usuário e senha")
        
    valida_usuario = user.autentica_usuario(usuario,senha)
    if valida_usuario:
        session['usuario_logado'] = request.form['usuario']
        flash(f'{session['usuario_logado']} logado com sucesso!')
        return redirect(url_for("lista_jogos"))
    else:
        flash('Usuario ou senha invalidos!')
        return redirect(url_for('login'))


#ROTA PARA DIRECIONAR TELA CADASTRO DE USUÁRIO
@app.route("/cadastro_usuario")
def cadastro_usuario():
    return render_template("cadastro_usuario.html",titulo = 'Cadastro Usuário')

#ROTA PARA CADASTRAR O USUÁRIO@
@app.route("/cadastrar_usuario",methods=['POST',])
def cadastrar_usuario():
    nome = request.form['nome']
    usuario = request.form['usuario']
    senha = request.form['senha']
    if nome == '' or usuario == '' or senha == '':
        flash("Favor preencher os 3 campos")
        return redirect(url_for("cadastro_usuario"))
    else:
        msg = user.criar_usuario(usuario,nome,senha)
        flash(msg)
        return redirect(url_for('login'))

#ROTA PARA DESLOGAR
@app.route("/logout",methods=['GET',])
@login_required
def logout():
    session.pop('usuario_logado', None)
    flash(f'logout efetuado com sucesso')
    return redirect(url_for("login"))
#ROTA PARA ALTERAR SENHA

#ROTA PARA EXCLUIR JOGO DA LISTA
@app.route("/excluir_jogo",methods=['POST',])
@login_required
def excluir_jogo():
        LISTA_JOGOS = lista_de_jogos()
        login = int(request.form['position'])
        msg = LISTA_JOGOS[login].deletar_jogo_bd()
        flash(msg)
        return redirect(url_for("lista_jogos"))


#ROTA IR PARA PAGINA ALTERAR SENHA
@app.route("/alterar_senha")
def pagina_altera_senha():
    return render_template("alterar_senha.html", titulo = 'Alterar Senha')

#ROTA PAGINA ALTERA SENHA PARA RETORNAR PARA LOGIN
@app.route("/retorna_login")
def retorna_tela_login():
    return redirect(url_for("login"))

#ROTA PARA ALTENTICAR NOVA SENHA
@app.route("/autenticar_nova_senha",methods=['POST',])
def altenticar_nova_senha_user():
    usuario = request.form['usuario']
    senha_antiga = request.form['senha_antiga']
    senha_nova = request.form['senha_nova']
    if usuario == '' or senha_antiga == '' or senha_nova == '':
        flash("Favor preencher os 3 campos")
        return redirect(url_for("alterar_senha"))
    else:
        msg = user.alterar_senha(usuario,senha_antiga,senha_nova)
        flash(msg)
        return redirect(url_for("login"))

@app.route("/excluir_usuario",methods=['POST',])
def excluir_usuario():
    usuario = request.form['usuario']
    senha = request.form['senha']
    if usuario == '' or senha == '':
        flash("Por gentileza adicionar usuário e senha para exclusão")
        return redirect(url_for("login"))
    else:
        msg = user.deleta_usuario(usuario,senha)
        flash(msg)
        return redirect(url_for("login"))

@app.route("/view_editar_jogo")
@login_required
def view_editar_jogo():
        LISTA_JOGOS = lista_de_jogos()
        index = int(request.args.get('position'))
        jogo = LISTA_JOGOS[index]
        return render_template("editar_jogos.html", titulo = 'Editar Jogo', jogo = jogo, index = index)

@app.route("/editar_jogo",methods=['POST',])
@login_required
def editar_jogo():
        LISTA_JOGOS = lista_de_jogos()
        nome = request.form['nome']
        print(nome)
        categoria = request.form['categoria']
        print(categoria)
        console = request.form['console']
        print(console)
        index = int(request.form['index'])
        jogo = LISTA_JOGOS[index].edita_jogo(nome,categoria,console)
        flash(jogo)
        return redirect(url_for('lista_jogos'))
