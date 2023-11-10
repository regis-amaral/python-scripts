import pdfplumber
import pandas as pd
from babel.numbers import format_currency

def extrair_tabelas(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Inicialize uma lista para armazenar todas as tabelas
        todas_tabelas = []

        # Itera sobre todas as páginas do PDF
        for pagina in pdf.pages:
            # Extraindo as tabelas da página atual
            tabelas_pagina = pagina.extract_tables()

            # Adiciona as tabelas à lista
            todas_tabelas.extend(tabelas_pagina)

        # Retorna a lista de tabelas
        return todas_tabelas

# Substitua 'caminho_para_seu_pdf.pdf' pelo caminho real do seu arquivo PDF
caminho_pdf = 'fatura-pdf/xp3.pdf'
tabelas = extrair_tabelas(caminho_pdf)

gastos = []

# Imprime as tabelas
for i, tabela in enumerate(tabelas):
    # Verifica se a tabela foi extraída corretamente e se contém a string "Data"
    if tabela and any("Data" in row for row in tabela):
        df = pd.DataFrame(tabela[1:], columns=tabela[0])

        # Imprime o DataFrame linha a linha, coluna a coluna
        for indice, linha in df.iterrows():
            # Verifica se a primeira coluna está no formato de data (22/10/23)
            if pd.to_datetime(linha.iloc[0], errors='coerce', dayfirst=True, format='%d/%m/%y') and pd.notna(pd.to_datetime(linha.iloc[0], errors='coerce', dayfirst=True, format='%d/%m/%y')):
                gastos.append([linha.iloc[0], linha.iloc[1], linha.iloc[2]])

# Imprime a lista de gastos de forma mais legível
total = 0.0
for i, gasto in enumerate(gastos):
    if "Pagamentos Validos Normais" not in gasto[1]:
        print(f"{gasto[0]} {gasto[1]}   {gasto[2]}")    
        valor = gasto[2].replace('.', '').replace(',', '.') 
        total += float(valor)

# Formata o total da fatura em reais (R$) usando babel
total_formatado = format_currency(total, 'BRL', locale='pt_BR')
print("Total da fatura:", total_formatado)