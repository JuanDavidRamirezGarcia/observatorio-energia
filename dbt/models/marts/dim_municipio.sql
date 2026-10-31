{{ config(materialized='table') }}

with municipios_unicos as (
    select distinct
        divipola,
        municipio
    from {{ source('silver', 'enerandes_ventas') }}
    where divipola is not null
)
select
    row_number() over (order by divipola) as municipio_id,
    divipola,
    municipio,
    'Antioquia' as departamento
from municipios_unicos
