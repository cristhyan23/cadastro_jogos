from dotenv import load_dotenv
import mysql.connector
import os
from bd.jogo import Jogo
from bd.conexao_bd import IntegracaoBD

class ListadorJogos(IntegracaoBD):
    def __init__(self):
        super().__init__()

    

    def select_jogos(self,usuario):
        try:
            LISTA_JOGOS = []
            # Criar um cursor
            cursor = self.conexao.cursor()

            #captura ID USUARIOS
            consulta_id_usuario = "SELECT id FROM login WHERE usuario = %s"
            cursor.execute(consulta_id_usuario,(usuario,))
            id_usuario = cursor.fetchall()[0]
            # Inserir o novo usuário na tabela "login"
            sql = "SELECT * FROM jogos WHERE id_usuario = %s"
            cursor.execute(sql,(id_usuario[0],))
        
            # Recuperar os resultados
            resultados = cursor.fetchall()
            for row in resultados:
                #mostra primeira e segunda coluna somente
                LISTA_JOGOS.append(Jogo(row[1], row[2], row[3],usuario))

        except mysql.connector.Error as erro:
            print("Erro ao procurar jogos:", erro)

        finally:
            # Fechar o cursor e a conexão
            if 'conexao' in locals() or 'conexao' in globals():
                cursor.close()
                self.conexao.close()
            
            return LISTA_JOGOS

if __name__ =="__main__":
    # Carregar as variáveis de ambiente
    selecionador = ListadorJogos()
    jogos = selecionador.select_jogos("usuario_teste3")
    for jogo in jogos:
        print(jogo.get_name)