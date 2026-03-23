# 🛥️ LH Nautical - Data Lakehouse & Inteligência de Negócios

## 📌 Propósito
Este repositório reúne a solução de dados desenvolvida para a LH Nautical. O objetivo foi transformar dados descentralizados e conflitantes em informações confiáveis, automatizadas e prontas para tomada de decisão estratégica.

A entrega inclui:
- pipeline de dados completo (da ingestão à camada analítica)
- métricas financeiras validadas (receita, custo e margem)
- segmentação de clientes com recomendações operacionais
- relatórios e dashboards prontos para uso

---

## 🏗️ Arquitetura de Dados (Medallion)
O desenho segue o padrão bronze-prata-ouro, com foco em rastreabilidade e qualidade:
- Bronze: ingestão de arquivos originais (`.csv`, `.json`), sem alterações.
- Prata: limpeza, normalização e modelagem dimensional.
- Ouro: tabelas de métricas, visão de profit e indicadores para negócio.

Boas práticas adotadas:
- validação de dados e remoção de duplicados
- tratamento de formatos de data inconsistentes
- join ponto-a-ponto de histórico de custos e vendas

---

## 🧠 Machine Learning e Inteligência de Cliente
Segmentamos clientes usando RFM + K-Means e entregamos um roteiro simples de ações:
- Campeões (VIP): priorizar lançamentos e retenção premium.
- Regulares: reforçar cross-sell e up-sell.
- Em risco: ações de recuperação com ofertas específicas.

---

## 🛠️ Ferramentas
- Databricks / Spark (PySpark SQL)
- Python (Pandas, scikit-learn)
- Visualização e dashboards SQL

---

## ▶️ Guia rápido de execução
1. Carregue os arquivos de origem em `data_source/` no DBFS.
2. Execute os notebooks na ordem:
   1. `01_Tratamento_Produtos_Prata`
   2. `02_Tratamento_Clientes_Prata`
   3. `03_Tratamento_Vendas_Prata`
   4. `04_Tratamento_Custos_Prata`
   5. `05_Analise_Vendas_Ouro`
   6. `06_Relatorios_Executivos_Python`
   7. `07_Machine_Learning_Ouro`
   8. `08_Previsao_Demanda_Ouro`
3. Confira os resultados gerados e os dashboards de KPI.
4. Use as consultas em `sql_querys_for_dashboard/` para construir visualizações:
   - clientes por maior lucro acumulado
   - lucro por estado
   - ranking dos piores resultados
   - venda média por dia da semana

---

## 🎯 Resultados de negócio
- redução de retrabalho por dados inconsistentes
- visão clara de margem por cliente/produto
- plano de ação segmentado para comunicação e vendas

---

## 📎 Estrutura de arquivos
- `data_source/`: fontes originais (`clientes_crm.json`, `custos_importacao.json`, etc.)
- `notebooks/`: pipelines de transformação e análises
- `sql_querys_for_dashboard/`: queries prontas para dashboard
