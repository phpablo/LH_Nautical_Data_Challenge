# 🛥️ LH Nautical - Data Lakehouse & Inteligência de Negócio

## 📖 Visão Geral do Projeto
Este projeto foi desenvolvido para a **LH Nautical**, uma empresa do setor náutico que enfrentava desafios com dados descentralizados, sujos e sem visibilidade clara de margem de lucro e comportamento do cliente. 

O objetivo principal foi construir uma **Arquitetura de Dados de Ponta a Ponta (Medallion Architecture)** utilizando Databricks, saindo da ingestão de dados brutos até a criação de um motor de recomendação usando Machine Learning, gerando insights acionáveis para a diretoria.

---

## 🏗️ Arquitetura de Dados (Medallion Architecture)
O pipeline de dados foi desenhado seguindo as melhores práticas do Data Lakehouse, dividido em três camadas:

* **🥉 Camada Bronze (Ingestão):** Armazenamento dos dados brutos exatamente como foram extraídos dos sistemas de origem (arquivos CSV desestruturados e JSONs aninhados).
* **🥈 Camada Prata (Limpeza e Padronização):** * Uso intensivo de **Regex** para separar localizações complexas (Cidades vs. Portos).
    * Padronização de datas híbridas utilizando a função `COALESCE`.
    * Achatamento (Flattening) de arrays de custos históricos vindos de JSON utilizando a função `EXPLODE`.
* **🥇 Camada Ouro (Regras de Negócio e Analytics):**
    * Modelagem dimensional (Star Schema).
    * **Point-in-Time Joins:** Uso de Window Functions (`ROW_NUMBER()`) para cruzar a data exata da venda com o histórico de custos, garantindo o cálculo perfeito da Margem de Lucro.

---

## 🧠 Machine Learning & Segmentação de Clientes
Além da engenharia de dados, o projeto entregou valor de negócio através de Ciência de Dados:
1.  **Matriz RFM:** Cálculo de Recência, Frequência e Valor Monetário para cada cliente.
2.  **K-Means Clustering:** Uso do `scikit-learn` para segmentar os clientes em 3 grupos estratégicos baseados em similaridade matemática (dados escalonados via `StandardScaler`).
3.  **Recomendação Automatizada:**
    * **VIPs (Campeões):** Foco em exclusividade e acesso antecipado a produtos.
    * **Clientes Regulares:** Foco em campanhas de Cross-sell.
    * **Em Risco (Adormecidos):** Foco em retenção com descontos agressivos.

---

## 🛠️ Stack Tecnológica
* **Ambiente:** Databricks (Spark)
* **Engenharia de Dados:** SQL (PySpark SQL), CTEs, Window Functions, Regex.
* **Análise e Visualização:** Python, Pandas, Seaborn, Matplotlib e Dashboards SQL nativos do Databricks.
* **Machine Learning:** Scikit-Learn (K-Means).

---

## 🚀 Como Executar
1.  Acesse a pasta local de data_sources 
2.  Faça o upload dos arquivos `products.csv`, `sales.csv` e `costs.json` para o Databricks File System (DBFS) no formato de tabela.
3.  Execute os notebooks na seguinte ordem:
    * `01_Tratamento_Produtos_Prata` a `04_Tratamento_Custos_Prata` (SQL)
    * `05_Analise_Vendas_Ouro` (SQL)
    * `06_Relatorios_Executivos_Python` (Python/Pandas)
    * `07_Machine_Learning_Ouro` (Python/Scikit-Learn)
4. Acesse os dashboards SQL nativos do Databricks.
5. Vá na aba dashboards e crie 4 novas querys em SQL usando os arquivos da pasta `sql_querys_for_dashboard` para visualizar os insights de negócio.
6. Crie um dashboard usado como dataset as querys criadas anteriormente gerando  as seguintes visualizações:
    * Clientes maior lucro acumulado.
    * Distribuição de lucro por estado (Gráfico de pizza).
    * Ranking de piores resultados
    * Vendas media por dia da semana (Gráfico de barras).

---

## 💼 Impacto de Negócio
A solução entregou para a diretoria:
* **Confiabilidade:** Fim das divergências financeiras causadas por dados duplicados ou datas inválidas.
* **Visibilidade Financeira:** Dashboard consolidado de Receita e Lucro Bruto por produto e categoria.
* **Marketing Estratégico:** Fim do marketing genérico. A empresa agora sabe exatamente quem são seus clientes mais valiosos e quem está prestes a abandonar a marca, protegendo a margem de lucro.
