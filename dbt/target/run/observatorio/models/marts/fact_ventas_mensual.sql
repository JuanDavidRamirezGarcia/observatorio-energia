
    

    create  table
      "observatorio"."main"."fact_ventas_mensual__dbt_tmp"
  
    
    as (
      

select
    m_dim.mes_id,
    mun.municipio_id,
    seg.segmento_id,
    v.periodo,
    v.tipo_compra,
    v.energia_kwh,
    v.valor_cop,
    v.clientes
from 'data/silver/enerandes_ventas.parquet' v
left join "observatorio"."main"."dim_mes" m_dim 
    on v.periodo = m_dim.periodo
left join "observatorio"."main"."dim_municipio" mun 
    on v.divipola = mun.divipola
left join "observatorio"."main"."dim_segmento" seg 
    on v.segmento = seg.segmento and v.tipo_compra = seg.tipo_compra
    );
    
  