# Bitácora — Rober Castillo

**Rol:** Data Quality Analyst
**Rama de trabajo:** `transformar_rober`

| Fecha | Actividad | Detalle |
|---|---|---|
| 2026-10-25 | Ampliación del perfilamiento de la capa bronce | Se actualizó `docs/perfilamiento.md` para incluir los nueve archivos Parquet disponibles en `data/bronze/`. Se agregaron los perfiles de EnerAndes (2023–2026), IDEAM y NOAA, que faltaban en el resumen, y se actualizaron las cifras de los tres archivos XM según los datos locales. |
| 2026-10-25 | Análisis de estructura y calidad | Para cada archivo se registraron filas, columnas, duplicados exactos y cobertura temporal cuando fue posible; también se documentaron tipos y nulos por columna. Se identificaron 120 filas duplicadas y 148 celdas nulas en los cuatro archivos EnerAndes. Los campos heterogéneos de sus reportes anuales se señalaron como no normalizables para rango temporal sin limpiar encabezados y valores. |
| 2026-10-25 | Validación de resultados | Se contrastaron las métricas con los Parquet locales mediante pandas y se verificó que los nueve archivos de `data/bronze/` estén mencionados en el documento. |
| 2026-11-08 | Actualización de rama de trabajo | Se actualizó la rama de trabajo con `main` y se creó `transformar_rober` desde la versión vigente. Los cambios locales previos de muestras CSV se conservaron en un stash, sin mezclarlos con esta rama. |
| 2026-11-08 | Orquestación de Plata y Oro | Se modificó `src/transformar.py` para limpiar las fuentes y luego ejecutar `dbt build` desde la raíz del proyecto. Se configuró la ejecución para propagar errores de dbt y se agregó una prueba automatizada que verifica el orden de las operaciones. |
| 2026-11-08 | Exclusión de datos generados | Se verificó que `.gitignore` excluya `data/silver/` y los archivos `*.duckdb`; se eliminaron reglas duplicadas y se confirmó que no hay archivos de Plata o DuckDB versionados. |
| 2026-11-08 | Corrección de insumos faltantes para dbt | Al ejecutar el flujo, `dim_recurso` falló porque no existía `data/silver/xm_listado_recursos.parquet`. Se rastreó el origen a la ausencia de los insumos XM `xm_generacion`, `xm_aportes` y `xm_listado_recursos` en Bronce. El orquestador ahora ejecuta primero los extractores, que omiten los archivos existentes, y después limpia y construye las capas. Se actualizó la documentación de ejecución y la prueba del flujo; la prueba enfocada pasó. |
| 2026-11-08 | Publicación de cambios | Se registró y publicó en `origin/transformar_rober` el commit `ada0c24` (`Completa insumos faltantes antes de construir capas`). Los archivos temporales de `dbt/logs/` y `dbt/target/` permanecen locales y no forman parte del commit. |
