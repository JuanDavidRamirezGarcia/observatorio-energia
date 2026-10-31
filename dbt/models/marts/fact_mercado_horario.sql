{{ config(materialized='table') }}

select
    cast(strftime(p.fecha, '%Y%m%d') as integer) as fecha_key,
    p.fecha,
    p.hora,
    p.precio_bolsa_kwh,
    d.demanda_kwh
from {{ source('silver', 'xm_precio_bolsa') }} p
left join {{ source('silver', 'xm_demanda') }} d 
    on p.fecha = d.fecha and p.hora = d.hora