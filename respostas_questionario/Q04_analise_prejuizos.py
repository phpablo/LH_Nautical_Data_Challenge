import pandas as pd
import requests
import os
import warnings
warnings.filterwarnings("ignore")

print("1. Consumindo API de Dados Públicos do Banco Central (BCB)...")
url_bcb = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@dataInicial='01-01-2023'&@dataFinalCotacao='12-31-2024'&$top=10000&$format=json&$select=cotacaoVenda,dataHoraCotacao"
resposta = requests.get(url_bcb)
dados_bcb = resposta.json()['value']

df_dolar = pd.DataFrame(dados_bcb)
df_dolar['data_cotacao'] = pd.to_datetime(df_dolar['dataHoraCotacao']).dt.normalize()
df_dolar = df_dolar[['data_cotacao', 'cotacaoVenda']]

# Preenchendo dias sem cotação (finais de semana/feriados) com o valor do dia útil anterior
datas_completas = pd.date_range(start='2023-01-01', end='2024-12-31')
df_calendario = pd.DataFrame({'data_cotacao': datas_completas})
df_dolar = pd.merge(df_calendario, df_dolar, on='data_cotacao', how='left').ffill()

print("2. Lendo arquivos locais...")
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_vendas = os.path.join(diretorio_atual, '../data_source/vendas_2023_2024.csv')
caminho_custos = os.path.join(diretorio_atual, 'custos_importacao_normalizado.csv')

df_vendas = pd.read_csv(caminho_vendas)
df_custos = pd.read_csv(caminho_custos)

# Tratando a data usando o nome de coluna exato que você me passou
df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], dayfirst=True, errors='coerce')

print("3. Cruzando Vendas, Dólar e Custos...")
# Junta Vendas com Dólar do dia
df_vendas = pd.merge(df_vendas, df_dolar, left_on='sale_date', right_on='data_cotacao', how='left')

# Pegando os nomes dinâmicos do arquivo de custos normalizado
col_id_custos = next((col for col in df_custos.columns if 'id' in col.lower()), None)
col_usd_custos = next((col for col in df_custos.columns if 'usd' in col.lower() or 'price' in col.lower() or 'custo' in col.lower()), None)

# Pegando o custo de importação mais recente
df_custos_unicos = df_custos.drop_duplicates(subset=[col_id_custos], keep='last')
df_vendas = pd.merge(df_vendas, df_custos_unicos[[col_id_custos, col_usd_custos]], left_on='id_product', right_on=col_id_custos, how='left')

print("4. Executando as Regras de Negócio de Prejuízo...")
# Custo Transação BRL = (Custo Unitário USD * Quantidade Vendida) * Cotação do Dia
df_vendas['custo_total_brl'] = df_vendas[col_usd_custos] * df_vendas['qtd'] * df_vendas['cotacaoVenda']

# Lucro = Receita ('total') - Custo BRL
df_vendas['lucro_transacao'] = df_vendas['total'] - df_vendas['custo_total_brl']

# Isola apenas as perdas financeiras em valor absoluto
df_vendas['perda_brl'] = df_vendas['lucro_transacao'].apply(lambda x: abs(x) if x < 0 else 0)

# Agrega por Produto
df_agregado = df_vendas.groupby('id_product').agg(
    receita_total=('total', 'sum'),
    prejuizo_absoluto_total=('perda_brl', 'sum')
).reset_index()

# Calcula a Porcentagem de Perda
df_agregado['percentual_perda'] = (df_agregado['prejuizo_absoluto_total'] / df_agregado['receita_total']) * 100

# Filtra quem teve prejuízo e ordena pelo pior percentual
df_com_prejuizo = df_agregado[df_agregado['prejuizo_absoluto_total'] > 0]
df_ordenado = df_com_prejuizo.sort_values(by='percentual_perda', ascending=False)

print("\n--- RESULTADOS PARA A QUESTÃO 4 ---")
if not df_ordenado.empty:
    pior_produto = df_ordenado.iloc[0]
    print(f"-> ID do produto com maior % de perda relativa: {pior_produto['id_product']}")
    print(f"-> Porcentagem dessa perda: {pior_produto['percentual_perda']:.2f}%")
else:
    print("Incrível: Nenhum produto gerou prejuízo de acordo com essa base de dados!")