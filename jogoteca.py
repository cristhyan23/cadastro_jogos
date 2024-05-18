from dotenv import load_dotenv
import os
from flask import Flask, render_template,request,redirect,session,flash
from bd.jogo import Jogo
from bd.listador_jogos import ListadorJogos
from bd.usuario import Usuario
from functools import wraps
load_dotenv() # Carregar variáveis de ambiente do arquivo .env

#inicializa a aplicação flask
app = Flask(__name__,static_folder='static')
app.secret_key= os.getenv('SECRET_KEY')
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
def index():
    LISTA_JOGOS = lista_de_jogos()
     # devolve a lista de objeto jogo
    return render_template("lista.html", titulo = 'Jogos', jogos=LISTA_JOGOS,enumerate=enumerate) #mostra pagina html

#ROTA DIRECIONA PARA PAGINA CADASTRO
@app.route("/ir_cadastro", methods=['GET',])
def ir_cadastro():
    return redirect('/cadastro')

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
    return redirect("/lista_jogos") 

#PAGINA LOGIN
@app.route("/")
def login():
    return render_template("login.html")

#ROTA PARA LOGIN
@app.route("/autenticar", methods=['POST',])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']
    valida_usuario = user.autentica_usuario(usuario,senha)
    if valida_usuario:
        session['usuario_logado'] = request.form['usuario']
        flash(f'{session['usuario_logado']} logado com sucesso!')
        return redirect("/lista_jogos")
    else:
        flash('Usuario ou senha invalidos!')
        return redirect('/')


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
    msg = user.criar_usuario(usuario,nome,senha)
    flash(msg)
    return redirect("/")

#ROTA PARA DESLOGAR
@app.route("/logout",methods=['GET',])
@login_required
def logout():
    session.pop('usuario_logado', None)
    flash(f'logout efetuado com sucesso')
    return redirect("/")
#ROTA PARA ALTERAR SENHA

#ROTA PARA EXCLUIR JOGO DA LISTA
@app.route("/excluir_jogo",methods=['POST',])
@login_required
def excluir_jogo():
        LISTA_JOGOS = lista_de_jogos()
        index = int(request.form['position'])
        msg = LISTA_JOGOS[index].deletar_jogo_bd()
        flash(msg)
        return redirect("/lista_jogos")



#Roda a aplicação
if __name__ == "__main__":
    app.run(debug=True)
#debug para fazer as alterações automaticas e poder testar automaticamente


