
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select mes_id
from "observatorio"."main"."fact_ventas_mensual"
where mes_id is null



  
  
      
    ) dbt_internal_test