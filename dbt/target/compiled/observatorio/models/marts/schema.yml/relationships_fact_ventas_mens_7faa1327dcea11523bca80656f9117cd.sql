
    
    

with child as (
    select municipio_id as from_field
    from "observatorio"."main"."fact_ventas_mensual"
    where municipio_id is not null
),

parent as (
    select municipio_id as to_field
    from "observatorio"."main"."dim_municipio"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


