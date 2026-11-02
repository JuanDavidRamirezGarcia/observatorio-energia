
    
    

select
    mes_id as unique_field,
    count(*) as n_records

from "observatorio"."main"."dim_mes"
where mes_id is not null
group by mes_id
having count(*) > 1


