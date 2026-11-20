{{ config(materialized='table') }}

WITH source AS (
    SELECT *
    FROM {{ source('silver', 'noaa_oni') }}
)

SELECT
    CAST(periodo || '-01' AS DATE) AS fecha,
    CAST(oni AS DOUBLE) AS indice_oni,
    CASE
        WHEN CAST(oni AS DOUBLE) >= 0.5 THEN 'El Niño'
        WHEN CAST(oni AS DOUBLE) <= -0.5 THEN 'La Niña'
        ELSE 'Neutral'
    END AS fenomeno_climatologico
FROM source