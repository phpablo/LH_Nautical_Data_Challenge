import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

print("1. Carregando as Vendas...")
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_vendas = os.path.join(diretorio_atual, '../data_source/vendas_2023_2024.csv')
df_vendas = pd.read_csv(caminho_vendas)

# Garante que a data está no formato correto
df_vendas['sale_date'] = pd.to_datetime(df_vendas['sale_date'], dayfirst=True, errors='coerce')

print("2. Agrupando as vendas brutas por dia...")
vendas_por_dia = df_vendas.groupby('sale_date')['total'].sum().reset_index()

print("3. Criando a Máquina do Tempo (Calendário Completo)...")
# Pega o primeiro e o último dia do arquivo
data_min = vendas_por_dia['sale_date'].min()
data_max = vendas_por_dia['sale_date'].max()

# Cria uma lista ininterrupta de datas (inclusive os dias sem venda)
calendario_completo = pd.date_range(start=data_min, end=data_max)
df_calendario = pd.DataFrame({'sale_date': calendario_completo})

print("4. Cruzando o Calendário com as Vendas (O Pulo do Gato)...")
# LEFT JOIN: Traz o calendário inteiro e encaixa as vendas onde tiver. Onde não tiver, vira NaN.
df_completo = pd.merge(df_calendario, vendas_por_dia, on='sale_date', how='left')

# Preenche os "NaN" (dias sem venda) com ZERO Reais!
df_completo['total'] = df_completo['total'].fillna(0)

print("5. Calculando a Média Real por Dia da Semana...")
# Dicionário para traduzir os dias do inglês para o português
dias_pt = {
    'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
    'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
}
# Descobre o dia da semana e traduz
df_completo['dia_semana'] = df_completo['sale_date'].dt.day_name().map(dias_pt)

# Calcula a média MATEMATICAMENTE CORRETA
media_por_dia = df_completo.groupby('dia_semana')['total'].mean().reset_index()

# Ordena do Pior dia para o Melhor dia
media_por_dia = media_por_dia.sort_values(by='total', ascending=True)

print("\n--- RESULTADOS PARA A QUESTÃO 6.2 ---")
pior_dia = media_por_dia.iloc[0]
print(f"-> Pior dia da semana: {pior_dia['dia_semana']}")
print(f"-> Média de vendas desse dia: {pior_dia['total']:.2f}")