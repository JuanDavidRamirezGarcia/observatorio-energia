
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select segmento_id
from "observatorio"."main"."fact_ventas_mensual"
where segmento_id is null



  
  
      
    ) dbt_internal_test