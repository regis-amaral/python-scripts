import requests, psycopg2, urllib3, time
from datetime import datetime

urllib3.disable_warnings()

# Função para obter os resultados da API
def obter_resultados(id_concurso):
    url = f'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/{id_concurso}'
    response = requests.get(url, verify=False)
    return response.json()

# Função para conectar ao banco de dados PostgreSQL
def conectar_bd():
    conn = psycopg2.connect(
        dbname='loteria',
        user='postgres',
        password='postgres',
        host='localhost',
        port='5432'
    )
    return conn

# Função para inserir os resultados no banco de dados
def inserir_resultados(conn, concurso, data, dezenas_sorteadas):
    cursor = conn.cursor()
    
    data_apuracao = datetime.strptime(data, "%d/%m/%Y").date()

    # Convertendo dezenas_sorteadas para uma lista de inteiros
    dezenas_sorteadas = list(map(int, dezenas_sorteadas.split(',')))
    
    cursor.execute(
        'INSERT INTO lotofacil (concurso, data, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        [concurso, data_apuracao] + dezenas_sorteadas
    )
    conn.commit()
    cursor.close()

def resultado_existe_por_concurso(concurso):
    conn = conectar_bd()
    cursor = conn.cursor()
    # Execute a consulta SQL para verificar se o resultado existe
    cursor.execute("SELECT EXISTS (SELECT 1 FROM lotofacil WHERE concurso = %s)", (concurso,))
    resultado = cursor.fetchone()[0]  # Retorna True ou False
    cursor.close()
    conn.close()
    return resultado
        
codigos_com_erro = []

# Loop para obter e inserir os resultados
for id_concurso in range(2948, 0, -1):
    resultado = obter_resultados(id_concurso)
    try:
        if resultado_existe_por_concurso(id_concurso):
            continue
        tentativas = 0
        while tentativas < 5 and "dataApuracao" not in resultado:
            print(f"Serviço indisponível para o concurso {id_concurso}. Tentando novamente em 1 segundo...")
            time.sleep(1)
            resultado = obter_resultados(id_concurso)  # Tentar novamente
        if "dataApuracao" not in resultado:
            print("Não encontrado", id_concurso)
            codigos_com_erro.append(id_concurso)
            continue
        conn = conectar_bd()
        data_apuracao = resultado['dataApuracao']
        dezenas_sorteadas = ','.join(resultado['dezenasSorteadasOrdemSorteio'])
        inserir_resultados(conn, id_concurso, data_apuracao, dezenas_sorteadas)  
        print("Encontrado", id_concurso)
        conn.close()   
    except psycopg2.errors.UniqueViolation:
        continue
    except KeyError:
        print(KeyError)

if codigos_com_erro:
    print("Concursos não encontrados:")
    for codigo in codigos_com_erro:
        print(codigo)
