{{ config(materialized='table') }}

WITH precio_mensual AS (
    SELECT
        DATE_TRUNC('month', CAST(fecha AS DATE)) AS mes,
        AVG(CAST(precio_bolsa_kwh AS DOUBLE)) AS precio_bolsa_promedio
    FROM {{ source('silver', 'xm_precio_bolsa') }}
    GROUP BY 1
),

demanda_mensual AS (
    SELECT
        DATE_TRUNC('month', CAST(fecha AS DATE)) AS mes,
        SUM(CAST(demanda_kwh AS DOUBLE)) AS demanda_mensual_total
    FROM {{ source('silver', 'xm_demanda') }}
    GROUP BY 1
),

clima_mensual AS (
    SELECT
        DATE_TRUNC('month', CAST(fecha AS DATE)) AS mes,
        MAX(fenomeno_climatologico) AS fenomeno_climatologico
    FROM {{ ref('stg_clima_oni') }}
    GROUP BY 1
)

SELECT
    p.mes,
    p.precio_bolsa_promedio,
    d.demanda_mensual_total,
    c.fenomeno_climatologico
FROM precio_mensual AS p
LEFT JOIN demanda_mensual AS d
    ON p.mes = d.mes
LEFT JOIN clima_mensual AS c
    ON p.mes = c.mes
