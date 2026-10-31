

select
    cast(strftime(d.fecha, '%Y%m%d') as integer) as fecha_key,
    1 as recurso_key,
    d.fecha,
    d.hora,
    d.demanda_kwh as generacion_kwh
from 'data/silver/xm_demanda.parquet' d