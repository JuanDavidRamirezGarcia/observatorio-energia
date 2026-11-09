# Bitácora — Juan Fernando Cataño Higuita

Rol: Analytics Engineer

| Fecha | Actividad | Detalle |
|---|---|---|
| 2026-10-24 | Perfilamiento de la capa bronce | Se documentaron en `docs/perfilamiento.md` los archivos Parquet locales, su tamaño, columnas, tipos, nulos, duplicados y rango de fechas. |
| 2026-10-24 | Análisis de calidad de datos | Se registraron cinco hallazgos con evidencia numérica en `docs/perfilamiento.md`: duplicados y nulos en EnerAndes, diferencias de estructura entre archivos anuales, cobertura temporal incompleta de IDEAM y conteos `n_obs` atípicos a validar. |
| 2026-10-24 | Pruebas automatizadas del pipeline | Se añadieron pruebas con pytest para `ventanas()`, el aplanado de respuestas XM y la omisión de archivos existentes. Verificación: `python -m pytest -q` — 6 pruebas aprobadas. |
| 2026-11-01 | Documentación del modelo dimensional | Se creó `docs/modelo_dimensional.md` con el esquema estrella en Mermaid, la explicación del grano de cada tabla de hechos y la propuesta de dimensiones para fecha, hora, mercado, recurso, municipio y segmento. |
| 2026-11-01 | Diccionario de datos de la capa oro | Se creó `docs/diccionario_datos.md` con la definición de cada tabla del modelo oro: columnas, tipos, descripción y origen/fuente para `dim_fecha`, `dim_mes`, `dim_municipio`, `dim_segmento`, `dim_recurso`, `fact_ventas_mensual`, `fact_mercado_horario` y `fact_generacion_recurso`. |
| 2026-11-01 | Consultas analíticas de la capa oro | Se construyó la carpeta `consultas/oro/` con 3 consultas SQL para: ventas por municipio, comportamiento del precio de bolsa por hora y fase ENSO, y comparativo horario de generación vs demanda. |
| 2026-11-01 | Resultados y evidencias en README | Se agregaron en `README.md` los resultados ejecutados en DuckDB para las consultas de negocio, incluyendo rankings de consumo, precio promedio por hora y comparación de generación/demanda. |
| 2026-11-09 | Perfilamiento actualizado de la capa bronce | Se revisó y documentó el perfilamiento de los archivos Parquet locales en `docs/perfilamiento.md`, registrando filas, columnas, duplicados, nulos, tipos y rangos temporales de EnerAndes, IDEAM, NOAA y XM; además, se dejó evidencia de los hallazgos de calidad sobre estructura heterogénea y cobertura temporal incompleta. |
| 2026-11-09 | Validación pandera en la capa plata | Se implementaron esquemas de calidad con Pandera para todas las tablas de la capa plata en `src/quality/esquemas.py`, incluyendo reglas de tipo, rangos, valores aceptados y llaves únicas. Cada limpieza valida su DataFrame antes de guardarlo en `src/silver/enerandes.py`, `src/silver/noaa.py`, `src/silver/xm.py` y `src/silver/ideam.py`. |
| 2026-11-09 | Pruebas de reglas de limpieza | Se ampliaron las pruebas con casos de ejemplo pequeños y específicos en `tests/test_reglas_limpieza.py`: conversión MWh→kWh, parsing de fechas `mar-24` y `03/2024`, cálculo de la fase ENSO, normalización de segmentos y validación del pivote horizontal de XM a una fila por hora. Verificación: `python -m pytest -q` — 27 pruebas aprobadas. |
