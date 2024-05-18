# cadastro_jogos

é necessario ter um database em mySQL chamado: jogoteca com as seguintes tabelas:

tabela jogos:
primary key: id
Nome: VARCHAR(255)
Categoria: VARCHAR(255)
Console: VARCHAR(255)
id_usuario: VARCHAR(10)

tabela login:
primary key: id
usuario: VARCHAR(50)
senha: VARCHAR(50)
nome: VARCHAR(50)

também necessário adicionar um arquivo " .env "
com as seguintes configurações: 
# CHAVE SECRETA COOKIES
SECRET_KEY = "adcionar seu valor"

# CONEXÃO BANCO DE DADOS
DATABASE_PASSWORD = "adcionar seu valor"
DATABASE_USER = "adcionar seu valor"
DATABASE_HOST = "adcionar seu valor"
DATABASE_PORT = "adcionar seu valor"
DATABASE = "adcionar seu valor"
