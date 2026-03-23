import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_vendas = os.path.join(diretorio_atual, '../data_source/vendas_2023_2024.csv')
caminho_produtos = os.path.join(diretorio_atual, '../data_source/produtos_raw.csv')

df_vendas = pd.read_csv(caminho_vendas)
df_produtos = pd.read_csv(caminho_produtos)

# Limpeza
def limpar_categoria(cat):
    if pd.isna(cat): return cat
    cat_limpa = str(cat).lower().strip()
    if 'eletr' in cat_limpa: return 'eletrônicos'
    elif 'prop' in cat_limpa or 'motor' in cat_limpa: return 'propulsão'
    elif 'ancor' in cat_limpa or 'encor' in cat_limpa: return 'ancoragem'
    return cat_limpa

df_produtos['categoria_limpa'] = df_produtos['actual_category'].apply(limpar_categoria)

# Cruzamento de tabelas (code com id_product)
df_completo = pd.merge(df_vendas, df_produtos, left_on='id_product', right_on='code', how='left')

# Calculando Métricas
df_clientes = df_completo.groupby('id_client').agg(
    faturamento_total=('total', 'sum'),
    frequencia=('id', 'nunique'), # Número de transações únicas
    diversidade_categorias=('categoria_limpa', 'nunique') 
).reset_index()

df_clientes['ticket_medio'] = df_clientes['faturamento_total'] / df_clientes['frequencia']

# Filtrando Top 10 (3+ categorias)
df_elite = df_clientes[df_clientes['diversidade_categorias'] >= 3]
df_elite = df_elite.sort_values(by=['ticket_medio', 'id_client'], ascending=[False, True]).head(10)

# Isolando as vendas SÓ desses 10 clientes
df_vendas_top10 = df_completo[df_completo['id_client'].isin(df_elite['id_client'])]

# Achando a categoria mais vendida em Quantidade (qtd)
categoria_top = df_vendas_top10.groupby('categoria_limpa')['qtd'].sum().reset_index()
categoria_top = categoria_top.sort_values(by='qtd', ascending=False)

print("\n--- RESULTADO PARA A QUESTÃO 5.2 ---")
campea = categoria_top.iloc[0]
print(f"-> Categoria mais vendida: {campea['categoria_limpa']}")
print(f"-> Quantidade de itens: {campea['qtd']}")