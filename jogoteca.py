from dotenv import load_dotenv
import os
from flask import Flask

load_dotenv() # Carregar variáveis de ambiente do arquivo .env

#inicializa a aplicação flask
app = Flask(__name__,static_folder='static')
app.secret_key= os.getenv('SECRET_KEY')

#Roda a aplicação
if __name__ == "__main__":
    from views import *
    app.run(debug=True)
#debug para fazer as alterações automaticas e poder testar automaticamente


