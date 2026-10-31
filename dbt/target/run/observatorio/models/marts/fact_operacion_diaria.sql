
    

    create  table
      "observatorio"."main"."fact_operacion_diaria__dbt_tmp"
  
    
    as (
      

with precio as (
    select fecha, avg(precio_bolsa_kwh) as precio_bolsa_prom_dia
    from 'data/silver/xm_precio_bolsa.parquet'
    group by fecha
),
demanda as (
    select fecha, sum(demanda_kwh) as demanda_total_kwh_dia
    from 'data/silver/xm_demanda.parquet'
    group by fecha
),
embalses as (
    select fecha, volumen_util_pct
    from 'data/silver/xm_embalses.parquet'
)
select
    f.fecha_key,
    p.fecha,
    p.precio_bolsa_prom_dia,
    d.demanda_total_kwh_dia,
    e.volumen_util_pct
from precio p
left join "observatorio"."main"."dim_fecha" f on p.fecha = f.fecha
left join demanda d on p.fecha = d.fecha
left join embalses e on p.fecha = e.fecha
    );
    
  