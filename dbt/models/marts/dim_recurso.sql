{{ config(materialized='table') }}

with catalogo as (
    select distinct
        trim(cast(recurso_code as varchar)) as codigo_recurso,
        max(nullif(trim(recurso_name), '')) as nombre_recurso,
        max(nullif(trim(recurso_type), '')) as tipo_generacion,
        max(nullif(trim(recurso_enersource), '')) as fuente_energia,
        max(nullif(trim(recurso_companycode), '')) as empresa,
        max(nullif(trim(recurso_disp), '')) as disponibilidad,
        max(nullif(trim(recurso_state), '')) as estado
    from {{ source('silver', 'xm_listado_recursos') }}
    where recurso_code is not null
      and trim(cast(recurso_code as varchar)) <> ''
    group by trim(cast(recurso_code as varchar))
),
recursos_historicos as (
    select distinct
        trim(cast(g.code as varchar)) as codigo_recurso
    from {{ source('silver', 'xm_generacion') }} g
    left join catalogo c
        on trim(cast(g.code as varchar)) = c.codigo_recurso
    where g.code is not null
      and trim(cast(g.code as varchar)) <> ''
      and c.codigo_recurso is null
),
recursos as (
    select
        codigo_recurso,
        coalesce(nombre_recurso, codigo_recurso) as nombre_recurso,
        coalesce(tipo_generacion, 'NO IDENTIFICADO EN CATALOGO') as tipo_generacion,
        fuente_energia,
        empresa,
        disponibilidad,
        estado
    from catalogo
    union all
    select
        codigo_recurso,
        codigo_recurso as nombre_recurso,
        'NO IDENTIFICADO EN CATALOGO' as tipo_generacion,
        null as fuente_energia,
        'XM' as empresa,
        null as disponibilidad,
        null as estado
    from recursos_historicos
)
select
    row_number() over (order by codigo_recurso) as recurso_key,
    *
from recursos