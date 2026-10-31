
    

    create  table
      "observatorio"."main"."fact_clima_diario__dbt_tmp"
  
    
    as (
      

with prec as (
    select fecha, avg(precipitacion_mm) as precipitacion_prom_mm
    from 'data/silver/ideam_precipitacion.parquet'
    group by fecha
),
temp as (
    select fecha, avg(temperatura_c) as temperatura_prom_c
    from 'data/silver/ideam_temperatura.parquet'
    group by fecha
)
select
    f.fecha_key,
    p.fecha,
    p.precipitacion_prom_mm,
    t.temperatura_prom_c
from prec p
left join "observatorio"."main"."dim_fecha" f on p.fecha = f.fecha
left join temp t on p.fecha = t.fecha
    );
    
  