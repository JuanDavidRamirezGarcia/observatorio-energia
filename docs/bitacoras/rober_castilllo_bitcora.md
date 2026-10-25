# Bitácora — Rober Castillo

**Rol:** Data Quality Analyst
**Rama de trabajo:** `rober_Data-Quality-Analyst`

| Fecha | Actividad | Detalle |
|---|---|---|
| 2026-10-25 | Ampliación del perfilamiento de la capa bronce | Se actualizó `docs/perfilamiento.md` para incluir los nueve archivos Parquet disponibles en `data/bronze/`. Se agregaron los perfiles de EnerAndes (2023–2026), IDEAM y NOAA, que faltaban en el resumen, y se actualizaron las cifras de los tres archivos XM según los datos locales. |
| 2026-10-25 | Análisis de estructura y calidad | Para cada archivo se registraron filas, columnas, duplicados exactos y cobertura temporal cuando fue posible; también se documentaron tipos y nulos por columna. Se identificaron 120 filas duplicadas y 148 celdas nulas en los cuatro archivos EnerAndes. Los campos heterogéneos de sus reportes anuales se señalaron como no normalizables para rango temporal sin limpiar encabezados y valores. |
| 2026-10-25 | Validación de resultados | Se contrastaron las métricas con los Parquet locales mediante pandas y se verificó que los nueve archivos de `data/bronze/` estén mencionados en el documento. |