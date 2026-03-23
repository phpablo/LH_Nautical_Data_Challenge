SELECT 
    client_name AS Cliente,
    SUM(gross_profit) AS Lucro_Total_USD
FROM lh_nautical.lh_nautical_db.gld_lucro_detalhado
GROUP BY client_name
ORDER BY Lucro_Total_USD DESC
LIMIT 10;