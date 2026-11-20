WITH source AS (SELECT * FROM {{ source('silver', 'noaa_oni') }})
SELECT
CAST(fecha AS DATE) AS fecha,
CAST(valor_oni AS FLOAT64) AS indice_oni,
CASE
WHEN CAST(valor_oni AS FLOAT64) >= 0.5 THEN 'El Niño'
WHEN CAST(valor_oni AS FLOAT64) <= -0.5 THEN 'La Niña'
ELSE 'Neutral'
END AS fenomeno_climatologico
FROM source