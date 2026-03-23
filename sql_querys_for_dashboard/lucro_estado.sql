-- Lucro e quantidade de VIPs por Estado
SELECT 
    l.client_state AS Estado,
    SUM(l.gross_profit) AS Lucro_Total_USD,
    COUNT(DISTINCT l.id_client) AS Qtd_Clientes_Ativos
FROM lh_nautical.lh_nautical_db.gld_lucro_detalhado l
GROUP BY l.client_state
ORDER BY Lucro_Total_USD DESC;