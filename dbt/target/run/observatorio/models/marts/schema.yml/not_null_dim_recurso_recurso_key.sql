
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select recurso_key
from "observatorio"."main"."dim_recurso"
where recurso_key is null



  
  
      
    ) dbt_internal_test