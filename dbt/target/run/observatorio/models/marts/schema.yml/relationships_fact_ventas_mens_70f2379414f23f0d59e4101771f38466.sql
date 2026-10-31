
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select segmento_id as from_field
    from "observatorio"."main"."fact_ventas_mensual"
    where segmento_id is not null
),

parent as (
    select segmento_id as to_field
    from "observatorio"."main"."dim_segmento"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test