# Bitácora — Juan Fernando Cataño Higuita

Rol: Analytics Engineer

| Fecha | Actividad | Perfilamiento, bitácora y tests |
|24-10-2026|Perfilamiento, análisis y pruebas|---|
| 2026-10-24 | Perfilamiento de la capa bronce | Se documentaron en `docs/perfilamiento.md` los archivos Parquet locales, su tamaño, columnas, tipos, nulos, duplicados y rango de fechas. |
| 2026-10-24 | Análisis de calidad de datos | Se registraron cinco hallazgos con evidencia numérica en `docs/perfilamiento.md`: duplicados y nulos en EnerAndes, diferencias de estructura entre archivos anuales, cobertura temporal incompleta de IDEAM y conteos `n_obs` atípicos a validar. |
| 2026-10-24 | Pruebas automatizadas del pipeline | Se añadieron pruebas con pytest para `ventanas()`, el aplanado de respuestas XM y la omisión de archivos existentes. Verificación: `python -m pytest -q` — 6 pruebas aprobadas. |
