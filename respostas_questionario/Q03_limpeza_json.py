import pandas as pd
import json
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(diretorio_atual, '../data_source/custos_importacao.json')

try:
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    print("1. SUCESSO! JSON carregado.")
    
    # Investigação
    registros_limpos = []
    
    primeiro_item = dados[0]
    chave_lista = next((k for k, v in primeiro_item.items() if isinstance(v, list)), None)
    
    if chave_lista:
        print(f"2. Encontrei o array aninhado na chave: '{chave_lista}'")
        # Descompactando (Explode) o JSON
        for item in dados:
            # Pega as colunas base (como id_produto)
            base = {k: v for k, v in item.items() if k != chave_lista}
            
            # Para cada preço histórico dentro da lista, cria uma nova linha!
            for sub_item in item[chave_lista]:
                linha_final = base.copy()
                if isinstance(sub_item, dict):
                    linha_final.update(sub_item)
                else:
                    linha_final[chave_lista] = sub_item
                registros_limpos.append(linha_final)
                
        df_final = pd.DataFrame(registros_limpos)
    else:
        print("2. Não encontrei listas aninhadas. Carregando direto...")
        df_final = pd.DataFrame(dados)

    print(f"\n--- RESULTADO PARA A QUESTÃO 3.2 ---")
    print(f"Quantas entradas de importação o CSV recebeu ao todo? {len(df_final)}\n")
    
    # Criando o CSV 
    caminho_csv = os.path.join(diretorio_atual, 'custos_importacao_normalizado.csv')
    df_final.to_csv(caminho_csv, index=False)
    print(f"Tabela salva com sucesso em: {caminho_csv}")

except FileNotFoundError:
    print("ERRO: Não encontrei o arquivo 'custos_importacao.json'. Verifique a pasta data_source!")