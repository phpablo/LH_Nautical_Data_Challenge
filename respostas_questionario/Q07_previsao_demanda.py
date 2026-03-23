import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

print("1. Carregando e limpando dados...")
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_vendas = os.path.join(diretorio_atual, '../data_source/vendas_2023_2024.csv')
caminho_produtos = os.path.join(diretorio_atual, '../data_source/produtos_raw.csv')

df_vendas = pd.read_csv(caminho_vendas)
df_produtos = pd.read_csv(caminho_produtos)

# Tratamento de datas
df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], dayfirst=True, errors='coerce')

print("2. Isolando o Produto Alvo: Motor de Popa Yamaha...")
# Descobrindo o ID do motor especificado
id_motor = df_produtos[df_produtos['name'].str.contains('Motor de Popa Yamaha Evo Dash 155HP', case=False, na=False)]['code'].iloc[0]

# Filtrando só as vendas desse motor
df_motor = df_vendas[df_vendas['id_product'] == id_motor]
vendas_diarias = df_motor.groupby('sale_date')['qtd'].sum().reset_index()

print("3. Criando o Calendário de Treino (Até 31/12/2023)...")
calendario_treino = pd.date_range(start=vendas_diarias['sale_date'].min(), end='2023-12-31')
df_treino = pd.DataFrame({'sale_date': calendario_treino})
df_treino = pd.merge(df_treino, vendas_diarias, on='sale_date', how='left').fillna(0)

print("4. Construindo a Previsão Baseline (Média Móvel de 7 dias)...")
# A previsão de amanhã é a média dos últimos 7 dias. 
df_treino['previsao_baseline'] = df_treino['qtd'].rolling(window=7).mean().shift(1)

ultima_media_conhecida = df_treino.iloc[-1]['previsao_baseline']

# Criando os 7 primeiros dias de Janeiro
calendario_teste = pd.date_range(start='2024-01-01', end='2024-01-07')
df_previsao_janeiro = pd.DataFrame({
    'sale_date': calendario_teste,
    'previsao_vendas': ultima_media_conhecida
})

print("\n--- RESULTADOS PARA A QUESTÃO 7.2 ---")
soma_previsao = df_previsao_janeiro['previsao_vendas'].sum()
print(f"-> A previsão total de vendas para o Motor na primeira semana de Janeiro é: {round(soma_previsao)}")