import pandas as pd
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(diretorio_atual, 'produtos_raw.csv')

df_produtos = pd.read_csv(caminho_arquivo)

linhas_originais = len(df_produtos)

#  Removendo as duplicatas pelo ID do produto
df_produtos = df_produtos.drop_duplicates(subset=['code'], keep='first')
linhas_sem_duplicatas = len(df_produtos)
qtd_duplicatas_removidas = linhas_originais - linhas_sem_duplicatas

# Padronizando os nomes das categorias
def limpar_categoria(cat):
    if pd.isna(cat):
        return cat
    cat_limpa = str(cat).lower().strip()
    
    if 'eletr' in cat_limpa:
        return 'eletrônicos'
    elif 'prop' in cat_limpa or 'motor' in cat_limpa:
        return 'propulsão'
    elif 'ancor' in cat_limpa or 'encor' in cat_limpa:
        return 'ancoragem'
    else:
        return cat_limpa

if 'categoria' in df_produtos.columns:
    df_produtos['categoria'] = df_produtos['categoria'].apply(limpar_categoria)

# Convertendo valores para numérico
# Descobrindo o nome da coluna de preço (pode ser 'preco' ou 'valor')
col_preco = 'price'

if col_preco:
    df_produtos[col_preco] = df_produtos[col_preco].astype(str).str.replace('R$', '', regex=False)
    df_produtos[col_preco] = df_produtos[col_preco].str.replace(' ', '', regex=False)
    df_produtos[col_preco] = df_produtos[col_preco].str.replace(',', '.', regex=False)
    df_produtos[col_preco] = pd.to_numeric(df_produtos[col_preco], errors='coerce')

print(f"--- RESULTADO PARA A QUESTÃO 2.2 ---")
print(f"Quantos produtos duplicados foram removidos? {qtd_duplicatas_removidas}\n")