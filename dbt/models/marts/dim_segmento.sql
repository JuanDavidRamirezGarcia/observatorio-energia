{{ config(materialized='table') }}

with segmentos_unicos as (
    select distinct
        segmento,
        tipo_compra
    from {{ source('silver', 'enerandes_ventas') }}
    where segmento is not null
)
select
    row_number() over (order by segmento, tipo_compra) as segmento_id,
    segmento,
    tipo_compra
from segmentos_unicos
