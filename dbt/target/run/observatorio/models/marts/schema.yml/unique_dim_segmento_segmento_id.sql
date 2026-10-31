
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    segmento_id as unique_field,
    count(*) as n_records

from "observatorio"."main"."dim_segmento"
where segmento_id is not null
group by segmento_id
having count(*) > 1



  
  
      
    ) dbt_internal_test