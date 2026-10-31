

with municipios_unicos as (
    select distinct
        divipola,
        municipio
    from 'data/silver/enerandes_ventas.parquet'
    where divipola is not null
)
select
    row_number() over (order by divipola) as municipio_id,
    divipola,
    municipio,
    'Antioquia' as departamento
from municipios_unicos