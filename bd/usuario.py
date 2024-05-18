from dotenv import load_dotenv
import mysql.connector
import os
from bd.conexao_bd import IntegracaoBD
import hashlib #criptografar senha
load_dotenv() # Carregar variáveis de ambiente do arquivo .env

class Usuario(IntegracaoBD):

    def __init__(self):
        super().__init__()
    
#---------------------- FUNÇÕES PARA GESTÃO DE USUARIOS ----------------------------#

    def criar_usuario(self,usuario,nome,senha=123456):
        try:
            # Criar um cursor
            cursor = self.conexao.cursor()
            pwd =  hashlib.md5(senha.encode()).hexdigest() #é usado para calcular o hash MD5 da senha. Este hash terá sempre 32 caracteres hexadecimais,
            # Inserir o novo usuário na tabela "login"
            sql = "INSERT INTO login (usuario, senha,nome) VALUES (%s, %s,%s)"
            valores = (usuario, pwd,nome)
            cursor.execute(sql, valores)

            # Commit das mudanças
            self.conexao.commit()

            return "Usuário criado com sucesso!"

        except mysql.connector.Error as erro:
            return f"Erro ao criar usuário: {erro}"

        finally:
            # Fechar o cursor e a conexão
            if 'conexao' in locals() or 'conexao' in globals():
                cursor.close()
                self.conexao.close()

    def autentica_usuario(self,usuario,senha):
        try:
            # Criar um cursor
            cursor = self.conexao.cursor()
            pwd =  hashlib.md5(senha.encode()).hexdigest()
            # Inserir o novo usuário na tabela "login"
            sql = "SELECT * FROM login WHERE usuario = %s and senha = %s"
            valores = (usuario,pwd)
            cursor.execute(sql, valores)
            
            # Recuperar os resultados
            resultados = cursor.fetchall()
            if resultados:
                return True
            else:
                return False
            #for row in resultados:
                #mostra primeira e segunda coluna somente
            #    print(row[0],row[1])

        except mysql.connector.Error as erro:
            print("Erro ao procurar usuário:", erro)

        finally:
            # Fechar o cursor e a conexão
            if 'conexao' in locals() or 'conexao' in globals():
                cursor.close()
                self.conexao.close()

    def deleta_usuario(self,usuario):
        try:
            # Criar um cursor
            cursor = self.conexao.cursor()

            #Deletar usuário na tabela "login"
            sql = "DELETE FROM login WHERE usuario = %s"
            valores = (usuario,)
            cursor.execute(sql, valores)
            # Commit das mudanças
            self.conexao.commit()

            return "Usuário deletado com sucesso!"

        except mysql.connector.Error as erro:
            print("Erro ao deletar usuário:", erro)

        finally:
            # Fechar o cursor e a conexão
            if 'conexao' in locals() or 'conexao' in globals():
                cursor.close()
                self.conexao.close()

    def altera_senha(self,usuario,senha_velha,nova_senha):
        pass
# --------------------- FUNÇÕES PARA GESTÃO TABELA JOGOS -----------------------------#

# Exemplo de uso da função
if __name__ == '__main__':
    user = Usuario()
    #user.criar_usuario("usuario_teste3", "123")
    print(user.autentica_usuario("usuario_teste3", "123"))