import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings("ignore")

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_vendas = os.path.join(diretorio_atual, '../data_source/vendas_2023_2024.csv')
caminho_produtos = os.path.join(diretorio_atual, '../data_source/produtos_raw.csv')

df_vendas = pd.read_csv(caminho_vendas)
df_produtos = pd.read_csv(caminho_produtos)

# 1. Consertando o erro do Edital: O alvo real é o Vortex Maré Drift
nome_alvo = "GPS Garmin Vortex Maré Drift"
id_alvo = df_produtos[df_produtos['name'] == nome_alvo]['code'].iloc[0]

print(f"1. O ID do produto alvo ({nome_alvo}) é: {id_alvo}")

# 2. Criando a Matriz Usuário x Produto usando o ID_PRODUCT (que é o que a questão pede)
df_vendas['comprou'] = 1
matriz_interacao = df_vendas.pivot_table(index='id_client', columns='id_product', values='comprou', aggfunc='max').fillna(0)

# 3. Similaridade de Cosseno
matriz_produtos = matriz_interacao.T
similaridade_array = cosine_similarity(matriz_produtos)
df_similaridade = pd.DataFrame(similaridade_array, index=matriz_produtos.index, columns=matriz_produtos.index)

# 4. Achando o Par Perfeito
recomendacoes = df_similaridade[id_alvo].sort_values(ascending=False)
id_mais_similar = recomendacoes.index[1] # O índice 0 é ele mesmo (score 1.0)
score = recomendacoes.iloc[1]

# Nome do produto recomendado para o nosso conhecimento
nome_recomendado = df_produtos[df_produtos['code'] == id_mais_similar]['name'].iloc[0]

print("\n--- RESULTADOS PARA A QUESTÃO 8.2 ---")
print(f"-> ID_PRODUTO COM MAIOR SIMILARIDADE: {id_mais_similar}")
print(f"-> Nome do Produto: '{nome_recomendado}'")
print(f"-> Score de similaridade: {score:.4f}")