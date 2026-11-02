WITH oni AS (
    SELECT
        YR AS anio,
        CASE
            WHEN AVG(CAST(ANOM AS DOUBLE)) > 0.5 THEN 'El Niño'
            WHEN AVG(CAST(ANOM AS DOUBLE)) < -0.5 THEN 'La Niña'
            ELSE 'Neutro'
        END AS fase_enso
    FROM read_parquet('data/bronze/noaa_oni.parquet')
    GROUP BY YR
)
SELECT
    m.hora,
    oni.fase_enso,
    ROUND(AVG(m.precio_bolsa_cop_kwh), 2) AS precio_promedio_cop_kwh
FROM fact_mercado_horario m
JOIN dim_fecha d ON d.fecha_key = m.fecha_key
LEFT JOIN oni ON oni.anio = d.anio
GROUP BY m.hora, oni.fase_enso
ORDER BY oni.fase_enso, m.hora;
