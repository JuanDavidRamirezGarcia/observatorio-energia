
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select fecha_key
from "observatorio"."main"."fact_mercado_horario"
where fecha_key is null



  
  
      
    ) dbt_internal_test