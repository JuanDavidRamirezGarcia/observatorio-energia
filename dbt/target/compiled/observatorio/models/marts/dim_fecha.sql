

with rango_fechas as (
    select unnest(generate_series(date '2023-01-01', date '2026-12-31', interval '1 day')) as fecha
),
noaa as (
    select distinct periodo, fase_enso 
    from 'data/silver/noaa_oni.parquet'
)
select
    cast(strftime(rf.fecha, '%Y%m%d') as integer) as fecha_key,
    rf.fecha,
    year(rf.fecha) as anio,
    month(rf.fecha) as mes,
    day(rf.fecha) as dia,
    strftime(rf.fecha, '%Y-%m') as periodo_yyyy_mm,
    quarter(rf.fecha) as trimestre,
    dayofweek(rf.fecha) as dia_semana,
    coalesce(n.fase_enso, 'Neutral') as fase_enso
from rango_fechas rf
left join noaa n on strftime(rf.fecha, '%Y-%m') = n.periodo