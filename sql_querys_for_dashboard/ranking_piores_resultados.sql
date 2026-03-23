SELECT 
    product_name AS Produto,
    SUM(gross_profit) AS Resultado_Acumulado_USD
FROM lh_nautical.lh_nautical_db.gld_lucro_detalhado
GROUP BY product_name
ORDER BY Resultado_Acumulado_USD ASC
LIMIT 10;