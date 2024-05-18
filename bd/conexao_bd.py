from dotenv import load_dotenv
import mysql.connector
import os
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class IntegracaoBD:
    def __init__(self):
        self.conexao = self._conexao_bd()
    
    # Conectar ao banco de dados
    def _conexao_bd(self):
        try:
            conexao = mysql.connector.connect(
                host= os.getenv('DATABASE_HOST'),
                user=os.getenv('DATABASE_USER'),
                port=os.getenv('DATABASE_PORT'),
                password=os.getenv('DATABASE_PASSWORD'),
                database=os.getenv('DATABASE'),  # substitua pelo nome do seu banco de dados
                auth_plugin='mysql_native_password'
            )
            return conexao
        except mysql.connector.Error as erro:
            print(f'Erro: {erro}')
# --