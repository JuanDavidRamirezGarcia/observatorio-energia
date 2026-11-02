
    
    

with all_values as (

    select
        tipo_compra as value_field,
        count(*) as n_records

    from "observatorio"."main"."fact_ventas_mensual"
    group by tipo_compra

)

select *
from all_values
where value_field not in (
    'Bolsa','Contrato'
)


