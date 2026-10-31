{{ config(materialized='table') }}

with recursos as (
    select distinct
        'REC_EMBALSE' as codigo_recurso,
        'Sistema Embalses XM' as nombre_recurso,
        'Hidráulico' as tipo_generacion,
        'XM' as empresa
    from {{ source('silver', 'xm_embalses') }}
)
select
    1 as recurso_key,
    codigo_recurso,
    nombre_recurso,
    tipo_generacion,
    empresa
from recursos