
    
    

select
    segmento_id as unique_field,
    count(*) as n_records

from "observatorio"."main"."dim_segmento"
where segmento_id is not null
group by segmento_id
having count(*) > 1


