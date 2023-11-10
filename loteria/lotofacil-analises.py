from sqlalchemy import create_engine, MetaData, Table, select

from conexao_bd import ConexaoBD

conn = ConexaoBD.conectar()

# Definir a tabela
lotofacil = Table('lotofacil', metadata, autoload=True, autoload_with=engine)

# Criar uma consulta para selecionar todos os dados
consulta = select([lotofacil])

# Executar a consulta
conn = engine.connect()
resultados = conn.execute(consulta)

# Obter todos os dados
dados = resultados.fetchall()

# Fechar a conexão
conn.close()

# Agora, 'dados' contém todos os registros da tabela 'lotofacil'
