import psycopg2

class ConexaoBD:
    @staticmethod
    def conectar():
        conn = psycopg2.connect(
            dbname='loteria',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        return conn
