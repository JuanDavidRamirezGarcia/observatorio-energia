
    
    

select
    municipio_id as unique_field,
    count(*) as n_records

from "observatorio"."main"."dim_municipio"
where municipio_id is not null
group by municipio_id
having count(*) > 1


