SELECT
    m.municipio,
    ROUND(SUM(f.energia_kwh) / 1000000.0, 2) AS consumo_gwh
FROM fact_ventas_mensual f
JOIN dim_municipio m ON m.municipio_id = f.municipio_id
GROUP BY m.municipio
ORDER BY consumo_gwh DESC
LIMIT 10;
