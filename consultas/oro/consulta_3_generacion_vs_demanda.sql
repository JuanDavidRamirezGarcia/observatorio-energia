SELECT
    g.hora,
    ROUND(AVG(g.generacion_kwh) / 1000000.0, 2) AS generacion_mwh,
    ROUND(AVG(m.demanda_kwh) / 1000000.0, 2) AS demanda_mwh,
    ROUND((AVG(g.generacion_kwh) - AVG(m.demanda_kwh)) / 1000000.0, 2) AS diferencia_mwh
FROM fact_generacion_recurso g
JOIN fact_mercado_horario m
    ON m.fecha_key = g.fecha_key
   AND m.hora = g.hora
GROUP BY g.hora
ORDER BY g.hora;
