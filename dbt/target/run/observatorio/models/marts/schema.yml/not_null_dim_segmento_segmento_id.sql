
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select segmento_id
from "observatorio"."main"."dim_segmento"
where segmento_id is null



  
  
      
    ) dbt_internal_test