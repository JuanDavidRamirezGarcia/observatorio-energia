
    

    create  table
      "observatorio"."main"."dim_fuente__dbt_tmp"
  
    
    as (
      

select 1 as fuente_key, 'EnerAndes' as nombre_fuente, 'Ventas de Energía' as descripcion
union all
select 2, 'XM', 'Mercado Mayorista y Sistema Interconectado'
union all
select 3, 'NOAA', 'Índice Oceánico El Niño (ONI)'
union all
select 4, 'IDEAM', 'Estaciones Climatológicas Antioquia'
    );
    
  