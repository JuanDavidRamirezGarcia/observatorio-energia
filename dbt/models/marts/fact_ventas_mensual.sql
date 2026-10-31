{{ config(materialized='table') }}

select
    m_dim.mes_id,
    mun.municipio_id,
    seg.segmento_id,
    v.periodo,
    v.tipo_compra,
    v.energia_kwh,
    v.valor_cop,
    v.clientes
from {{ source('silver', 'enerandes_ventas') }} v
left join {{ ref('dim_mes') }} m_dim 
    on v.periodo = m_dim.periodo
left join {{ ref('dim_municipio') }} mun 
    on v.divipola = mun.divipola
left join {{ ref('dim_segmento') }} seg 
    on v.segmento = seg.segmento and v.tipo_compra = seg.tipo_compra