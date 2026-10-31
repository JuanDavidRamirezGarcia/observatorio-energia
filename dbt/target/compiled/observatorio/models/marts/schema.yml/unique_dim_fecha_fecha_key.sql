
    
    

select
    fecha_key as unique_field,
    count(*) as n_records

from "observatorio"."main"."dim_fecha"
where fecha_key is not null
group by fecha_key
having count(*) > 1


