
    

    create  table
      "observatorio"."main"."dim_segmento__dbt_tmp"
  
    
    as (
      

with segmentos_unicos as (
    select distinct
        segmento,
        tipo_compra
    from 'data/silver/enerandes_ventas.parquet'
    where segmento is not null
)
select
    row_number() over (order by segmento, tipo_compra) as segmento_id,
    segmento,
    tipo_compra
from segmentos_unicos
    );
    
  