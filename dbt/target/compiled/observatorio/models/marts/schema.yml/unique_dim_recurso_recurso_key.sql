
    
    

select
    recurso_key as unique_field,
    count(*) as n_records

from "observatorio"."main"."dim_recurso"
where recurso_key is not null
group by recurso_key
having count(*) > 1


