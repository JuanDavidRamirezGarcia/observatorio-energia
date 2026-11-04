{{ config(materialized='table') }}

select
    cast(strftime(g.fecha, '%Y%m%d') as integer) as fecha_key,
    r.recurso_key,
    g.fecha,
    g.hora,
    r.codigo_recurso,
    g.generacion_mwh
from {{ source('silver', 'xm_generacion') }} g
left join {{ ref('dim_recurso') }} r
    on trim(cast(g.code as varchar)) = r.codigo_recurso