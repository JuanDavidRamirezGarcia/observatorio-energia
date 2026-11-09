WITH oni AS (
    SELECT
        periodo,
        fase_enso
    FROM read_parquet('data/silver/noaa_oni.parquet')
)
SELECT
    m.hora,
    COALESCE(d.fase_enso, 'Neutral') AS fase_enso,
    ROUND(AVG(m.precio_bolsa_kwh), 2) AS precio_promedio_cop_kwh
FROM fact_mercado_horario m
JOIN dim_fecha d ON d.fecha_key = m.fecha_key
GROUP BY m.hora, d.fase_enso
ORDER BY d.fase_enso, m.hora;
