# Perfilamiento de la capa bronce

Este documento fue generado automáticamente desde todos los archivos Parquet en `data/bronze/`.

## Resumen ejecutivo

| Archivo | Filas | Columnas | Duplicadas exactas | Cobertura temporal | Tamaño estimado |
|---|---:|---:|---:|---|---:|
| `enerandes_ventas_2023.parquet` | 1,114 | 10 | 32 | Sin rango normalizable | 32.8 KB |
| `enerandes_ventas_2024.parquet` | 1,114 | 11 | 32 | Sin rango normalizable | 34.6 KB |
| `enerandes_ventas_2025.parquet` | 1,117 | 10 | 32 | Sin rango normalizable | 33.1 KB |
| `enerandes_ventas_2026.parquet` | 839 | 10 | 24 | Sin rango normalizable | 26.6 KB |
| `ideam_precipitacion_diaria.parquet` | 18,221 | 11 | 0 | 2025-01-01 a 2025-12-31 | 66.8 KB |
| `ideam_temperatura_diaria.parquet` | 10,772 | 13 | 0 | 2025-01-01 a 2025-12-31 | 113.6 KB |
| `noaa_oni.parquet` | 921 | 7 | 0 | 1950-01-01 a 2026-01-01 | 9.6 KB |
| `trm_colombia.parquet` | 649 | 7 | 0 | 2024-01-03 a 2026-09-30 | 17.1 KB |
| `xm_aportes.parquet` | 1,004 | 6 | 0 | 2024-01-01 a 2026-09-30 | 20.1 KB |
| `xm_demanda.parquet` | 1,004 | 30 | 0 | 2024-01-01 a 2026-09-30 | 282.6 KB |
| `xm_embalses.parquet` | 1,004 | 6 | 0 | 2024-01-01 a 2026-09-30 | 15.9 KB |
| `xm_generacion.parquet` | 350,361 | 30 | 0 | 2024-01-01 a 2026-09-30 | 43127.0 KB |
| `xm_listado_recursos.parquet` | 2,502 | 5 | 2 | Sin rango normalizable | 71.9 KB |
| `xm_precio_bolsa.parquet` | 1,004 | 30 | 0 | 2024-01-01 a 2026-09-30 | 261.0 KB |

## Detalle por archivo

### `enerandes_ventas_2023.parquet`

- Filas: 1,114
- Columnas: 10
- Filas duplicadas exactas: 32
- Cobertura temporal: Sin rango normalizable

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `col_0` | `str` | 0.00 |
| `col_1` | `str` | 0.09 |
| `col_2` | `str` | 1.44 |
| `col_3` | `str` | 0.09 |
| `col_4` | `str` | 0.90 |
| `col_5` | `str` | 0.72 |
| `col_6` | `str` | 0.09 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `enerandes_ventas_2024.parquet`

- Filas: 1,114
- Columnas: 11
- Filas duplicadas exactas: 32
- Cobertura temporal: Sin rango normalizable

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `col_0` | `str` | 0.00 |
| `col_1` | `str` | 0.09 |
| `col_2` | `str` | 0.36 |
| `col_3` | `str` | 0.09 |
| `col_4` | `str` | 0.72 |
| `col_5` | `str` | 0.09 |
| `col_6` | `str` | 1.08 |
| `col_7` | `str` | 0.09 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `enerandes_ventas_2025.parquet`

- Filas: 1,117
- Columnas: 10
- Filas duplicadas exactas: 32
- Cobertura temporal: Sin rango normalizable

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `col_0` | `str` | 0.09 |
| `col_1` | `str` | 0.36 |
| `col_2` | `str` | 0.90 |
| `col_3` | `str` | 0.36 |
| `col_4` | `str` | 0.90 |
| `col_5` | `str` | 0.72 |
| `col_6` | `str` | 0.36 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `enerandes_ventas_2026.parquet`

- Filas: 839
- Columnas: 10
- Filas duplicadas exactas: 24
- Cobertura temporal: Sin rango normalizable

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `col_0` | `str` | 0.12 |
| `col_1` | `str` | 0.48 |
| `col_2` | `str` | 1.07 |
| `col_3` | `str` | 0.48 |
| `col_4` | `str` | 1.07 |
| `col_5` | `str` | 1.31 |
| `col_6` | `str` | 0.48 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `ideam_precipitacion_diaria.parquet`

- Filas: 18,221
- Columnas: 11
- Filas duplicadas exactas: 0
- Cobertura temporal: 2025-01-01 a 2025-12-31

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `codigoestacion` | `str` | 0.00 |
| `nombreestacion` | `str` | 0.00 |
| `municipio` | `str` | 0.00 |
| `latitud` | `str` | 0.00 |
| `longitud` | `str` | 0.00 |
| `fecha` | `str` | 0.00 |
| `precipitacion_mm` | `str` | 0.00 |
| `n_obs` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `ideam_temperatura_diaria.parquet`

- Filas: 10,772
- Columnas: 13
- Filas duplicadas exactas: 0
- Cobertura temporal: 2025-01-01 a 2025-12-31

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `codigoestacion` | `str` | 0.00 |
| `nombreestacion` | `str` | 0.00 |
| `municipio` | `str` | 0.00 |
| `latitud` | `str` | 0.00 |
| `longitud` | `str` | 0.00 |
| `fecha` | `str` | 0.00 |
| `temp_media` | `str` | 0.00 |
| `temp_min` | `str` | 0.00 |
| `temp_max` | `str` | 0.00 |
| `n_obs` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `noaa_oni.parquet`

- Filas: 921
- Columnas: 7
- Filas duplicadas exactas: 0
- Cobertura temporal: 1950-01-01 a 2026-01-01

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `SEAS` | `str` | 0.00 |
| `YR` | `str` | 0.00 |
| `TOTAL` | `str` | 0.00 |
| `ANOM` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `trm_colombia.parquet`

- Filas: 649
- Columnas: 7
- Filas duplicadas exactas: 0
- Cobertura temporal: 2024-01-03 a 2026-09-30

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `valor` | `str` | 0.00 |
| `unidad` | `str` | 0.00 |
| `vigenciadesde` | `str` | 0.00 |
| `vigenciahasta` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `xm_aportes.parquet`

- Filas: 1,004
- Columnas: 6
- Filas duplicadas exactas: 0
- Cobertura temporal: 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `Date` | `str` | 0.00 |
| `Id` | `str` | 0.00 |
| `Value` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `xm_demanda.parquet`

- Filas: 1,004
- Columnas: 30
- Filas duplicadas exactas: 0
- Cobertura temporal: 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `Date` | `str` | 0.00 |
| `Id` | `str` | 0.00 |
| `code` | `str` | 0.00 |
| `Hour01` | `str` | 0.00 |
| `Hour02` | `str` | 0.00 |
| `Hour03` | `str` | 0.00 |
| `Hour04` | `str` | 0.00 |
| `Hour05` | `str` | 0.00 |
| `Hour06` | `str` | 0.00 |
| `Hour07` | `str` | 0.00 |
| `Hour08` | `str` | 0.00 |
| `Hour09` | `str` | 0.00 |
| `Hour10` | `str` | 0.00 |
| `Hour11` | `str` | 0.00 |
| `Hour12` | `str` | 0.00 |
| `Hour13` | `str` | 0.00 |
| `Hour14` | `str` | 0.00 |
| `Hour15` | `str` | 0.00 |
| `Hour16` | `str` | 0.00 |
| `Hour17` | `str` | 0.00 |
| `Hour18` | `str` | 0.00 |
| `Hour19` | `str` | 0.00 |
| `Hour20` | `str` | 0.00 |
| `Hour21` | `str` | 0.00 |
| `Hour22` | `str` | 0.00 |
| `Hour23` | `str` | 0.00 |
| `Hour24` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `xm_embalses.parquet`

- Filas: 1,004
- Columnas: 6
- Filas duplicadas exactas: 0
- Cobertura temporal: 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `Date` | `str` | 0.00 |
| `Id` | `str` | 0.00 |
| `Value` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `xm_generacion.parquet`

- Filas: 350,361
- Columnas: 30
- Filas duplicadas exactas: 0
- Cobertura temporal: 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `Date` | `str` | 0.00 |
| `Id` | `str` | 0.00 |
| `code` | `str` | 0.00 |
| `Hour01` | `str` | 0.00 |
| `Hour02` | `str` | 0.00 |
| `Hour03` | `str` | 0.00 |
| `Hour04` | `str` | 0.00 |
| `Hour05` | `str` | 0.00 |
| `Hour06` | `str` | 0.00 |
| `Hour07` | `str` | 0.00 |
| `Hour08` | `str` | 0.00 |
| `Hour09` | `str` | 0.00 |
| `Hour10` | `str` | 0.00 |
| `Hour11` | `str` | 0.00 |
| `Hour12` | `str` | 0.00 |
| `Hour13` | `str` | 0.00 |
| `Hour14` | `str` | 0.00 |
| `Hour15` | `str` | 0.00 |
| `Hour16` | `str` | 0.00 |
| `Hour17` | `str` | 0.00 |
| `Hour18` | `str` | 0.00 |
| `Hour19` | `str` | 0.00 |
| `Hour20` | `str` | 0.00 |
| `Hour21` | `str` | 0.00 |
| `Hour22` | `str` | 0.00 |
| `Hour23` | `str` | 0.00 |
| `Hour24` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `xm_listado_recursos.parquet`

- Filas: 2,502
- Columnas: 5
- Filas duplicadas exactas: 2
- Cobertura temporal: Sin rango normalizable

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `Id` | `str` | 0.00 |
| `Values` | `object` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |

### `xm_precio_bolsa.parquet`

- Filas: 1,004
- Columnas: 30
- Filas duplicadas exactas: 0
- Cobertura temporal: 2024-01-01 a 2026-09-30

| Columna | Tipo | Nulos (%) |
|---|---|---:|
| `Date` | `str` | 0.00 |
| `Id` | `str` | 0.00 |
| `code` | `str` | 0.00 |
| `Hour01` | `str` | 0.00 |
| `Hour02` | `str` | 0.00 |
| `Hour03` | `str` | 0.00 |
| `Hour04` | `str` | 0.00 |
| `Hour05` | `str` | 0.00 |
| `Hour06` | `str` | 0.00 |
| `Hour07` | `str` | 0.00 |
| `Hour08` | `str` | 0.00 |
| `Hour09` | `str` | 0.00 |
| `Hour10` | `str` | 0.00 |
| `Hour11` | `str` | 0.00 |
| `Hour12` | `str` | 0.00 |
| `Hour13` | `str` | 0.00 |
| `Hour14` | `str` | 0.00 |
| `Hour15` | `str` | 0.00 |
| `Hour16` | `str` | 0.00 |
| `Hour17` | `str` | 0.00 |
| `Hour18` | `str` | 0.00 |
| `Hour19` | `str` | 0.00 |
| `Hour20` | `str` | 0.00 |
| `Hour21` | `str` | 0.00 |
| `Hour22` | `str` | 0.00 |
| `Hour23` | `str` | 0.00 |
| `Hour24` | `str` | 0.00 |
| `_fuente` | `str` | 0.00 |
| `_origen` | `str` | 0.00 |
| `_extraido_en` | `str` | 0.00 |


## Hallazgos de calidad

| Hallazgo | Observación |
|---|---|
| Duplicados en `enerandes_ventas_2023.parquet` | Se detectaron 32 filas duplicadas exactas. |
| Nulos relevantes en `enerandes_ventas_2023.parquet` | La columna `col_2` tiene 1.44% de valores nulos. |
| Duplicados en `enerandes_ventas_2024.parquet` | Se detectaron 32 filas duplicadas exactas. |
| Nulos relevantes en `enerandes_ventas_2024.parquet` | La columna `col_6` tiene 1.08% de valores nulos. |
| Duplicados en `enerandes_ventas_2025.parquet` | Se detectaron 32 filas duplicadas exactas. |
| Nulos relevantes en `enerandes_ventas_2025.parquet` | La columna `col_2` tiene 0.90% de valores nulos. |
| Duplicados en `enerandes_ventas_2026.parquet` | Se detectaron 24 filas duplicadas exactas. |
| Nulos relevantes en `enerandes_ventas_2026.parquet` | La columna `col_5` tiene 1.31% de valores nulos. |
| Rango temporal en `ideam_precipitacion_diaria.parquet` | `fecha` cubre desde 2025-01-01 hasta 2025-12-31. |
| Rango temporal en `ideam_temperatura_diaria.parquet` | `fecha` cubre desde 2025-01-01 hasta 2025-12-31. |
| Rango temporal en `xm_aportes.parquet` | `Date` cubre desde 2024-01-01 hasta 2026-09-30. |
| Rango temporal en `xm_demanda.parquet` | `Date` cubre desde 2024-01-01 hasta 2026-09-30. |
| Rango temporal en `xm_embalses.parquet` | `Date` cubre desde 2024-01-01 hasta 2026-09-30. |
| Rango temporal en `xm_generacion.parquet` | `Date` cubre desde 2024-01-01 hasta 2026-09-30. |
| Duplicados en `xm_listado_recursos.parquet` | Se detectaron 2 filas duplicadas exactas. |
| Rango temporal en `xm_precio_bolsa.parquet` | `Date` cubre desde 2024-01-01 hasta 2026-09-30. |