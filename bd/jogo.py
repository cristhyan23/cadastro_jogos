from dotenv import load_dotenv
import mysql.connector
import os
from bd.conexao_bd import IntegracaoBD

class Jogo(IntegracaoBD):
    def __init__(self,nome,categoria, console,usuario):
        super().__init__()
        self._nome = nome
        self._categoria = categoria
        self._console=console
        self.usuario=usuario
        
    @property
    def get_name(self):
        return self._nome

    @property
    def get_category(self):
        return self._categoria
    
    @property
    def get_console(self):
        return self._console

    def salvar_jogo_bd(self):
        try:
            # Criar um cursor
            cursor = self.conexao.cursor()
            
            #captura ID USUARIOS
            consulta_id_usuario = "SELECT DISTINCT id FROM login WHERE usuario = %s"
            cursor.execute(consulta_id_usuario,(self.usuario,))
            id_usuario = cursor.fetchall()

            # Inserir o novo jogo na tabela "jogo"
            consulta_sql = "SELECT nome FROM jogos WHERE Nome = %s and id_usuario = %s "
            cursor.execute(consulta_sql, (self._nome,id_usuario[0][0]))
            resultados = cursor.fetchall()

            if len(resultados) == 0:
                sql = "INSERT INTO jogos (Nome, Categoria, Console,id_usuario) VALUES (%s, %s,%s,%s)"
                valores = (self._nome, self._categoria,self._console,id_usuario[0][0])
                cursor.execute(sql, valores)
                    # Commit das mudanças
                self.conexao.commit()
                return "Jogo salvo com sucesso!"
            else:
                return "Jogo já existe na base"
            

        except mysql.connector.Error as erro:
            print("Erro ao salvar jogo:", erro)

        finally:
            # Fechar o cursor e a conexão
            if 'conexao' in locals() or 'conexao' in globals():
                cursor.close()
                self.conexao.close()

    def deletar_jogo_bd(self):
        try:
            # Criar um cursor
            cursor = self.conexao.cursor()
            # Inserir o novo jogo na tabela "jogo"
            consulta_sql = "SELECT nome FROM jogos WHERE Nome = %s"
            cursor.execute(consulta_sql, (self._nome,))
            resultados = cursor.fetchall()
            
            consulta_id_usuario = "SELECT DISTINCT id FROM login WHERE usuario = %s"
            cursor.execute(consulta_id_usuario,(self.usuario,))
            id_usuario = cursor.fetchall()

            if len(resultados) > 0:
                sql = "DELETE FROM jogos WHERE Nome = %s AND Categoria = %s AND Console = %s AND id_usuario = %s"
                valores = (self._nome, self._categoria,self._console,id_usuario[0][0])
                cursor.execute(sql, valores)
                    # Commit das mudanças
                self.conexao.commit()
                return "Jogo deletado com sucesso!"
            else:
                return "Jogo não encontrado na base"
            

        except mysql.connector.Error as erro:
            print("Erro ao deletar jogo:", erro)

        finally:
            # Fechar o cursor e a conexão
            if 'conexao' in locals() or 'conexao' in globals():
                cursor.close()
                self.conexao.close()


if __name__ == '__main__':
    jogo = Jogo('God of War2','Rack n Slash','PS2','usuario_teste3')
    jogo.salvar_jogo_bd()
    print(jogo.get_name)
    jogo.deletar_jogo_bd()
   