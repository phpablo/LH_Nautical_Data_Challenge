WITH Calendario AS (
    -- Cria uma lista com TODOS os dias entre a primeira e a última venda
    SELECT explode(sequence(
        (SELECT MIN(sale_date) FROM lh_nautical.lh_nautical_db.gld_lucro_detalhado),
        (SELECT MAX(sale_date) FROM lh_nautical.lh_nautical_db.gld_lucro_detalhado),
        interval 1 day
    )) AS data_calendario
),
VendasDiarias AS (
    -- Soma as vendas de cada dia que realmente teve venda
    SELECT sale_date, SUM(gross_revenue) as total_vendido
    FROM lh_nautical.lh_nautical_db.gld_lucro_detalhado
    GROUP BY sale_date
),
CalendarioComVendas AS (
    -- Cruza o calendário completo com as vendas. Se não tem venda no dia, vira 0.
    SELECT 
        c.data_calendario,
        date_format(c.data_calendario, 'EEEE') AS nome_dia_semana,
        dayofweek(c.data_calendario) AS numero_dia_semana,
        COALESCE(v.total_vendido, 0) AS receita_diaria
    FROM Calendario c
    LEFT JOIN VendasDiarias v ON c.data_calendario = v.sale_date
)
-- Tira a média final por dia da semana!
SELECT 
    nome_dia_semana AS Dia_da_Semana,
    AVG(receita_diaria) AS Media_de_Vendas_USD
FROM CalendarioComVendas
GROUP BY nome_dia_semana, numero_dia_semana
ORDER BY numero_dia_semana;