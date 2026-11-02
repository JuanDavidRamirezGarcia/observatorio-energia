
    

    create  table
      "observatorio"."main"."fact_mercado_horario__dbt_tmp"
  
    
    as (
      

select
    cast(strftime(p.fecha, '%Y%m%d') as integer) as fecha_key,
    p.fecha,
    p.hora,
    p.precio_bolsa_kwh,
    d.demanda_kwh
from 'data/silver/xm_precio_bolsa.parquet' p
left join 'data/silver/xm_demanda.parquet' d 
    on p.fecha = d.fecha and p.hora = d.hora
    );
    
  