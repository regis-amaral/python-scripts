from sqlalchemy import create_engine, Column, Integer, MetaData, Table, Date

# Criar uma conexão com o banco de dados
engine = create_engine('postgresql://postgres:postgres@localhost/loteria')

# Criar um objeto MetaData
metadata = MetaData()

# Definir a classe que representa a tabela
class Lotofacil:
    __table__ = Table(
        'lotofacil',
        metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('concurso', Integer, unique=True, nullable=False),
        Column('data', Date, nullable=False),
        Column('n1', Integer, nullable=False),
        Column('n2', Integer, nullable=False),
        Column('n3', Integer, nullable=False),
        Column('n4', Integer, nullable=False),
        Column('n5', Integer, nullable=False),
        Column('n6', Integer, nullable=False),
        Column('n7', Integer, nullable=False),
        Column('n8', Integer, nullable=False),
        Column('n9', Integer, nullable=False),
        Column('n10', Integer, nullable=False),
        Column('n11', Integer, nullable=False),
        Column('n12', Integer, nullable=False),
        Column('n13', Integer, nullable=False),
        Column('n14', Integer, nullable=False),
        Column('n15', Integer, nullable=False)
    )

# Cria a tabela no banco de dados
metadata.create_all(bind=engine)