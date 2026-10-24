# Perfilamiento de la capa bronce

Este documento describe los archivos Parquet que estaban disponibles en
`data/bronze/` al momento de realizar el perfilamiento. La carpeta se genera
localmente al ejecutar el pipeline y está excluida de Git, por lo que los
resultados pueden cambiar cuando se vuelvan a descargar los datos.

## Resumen por archivo

| Archivo | Filas | Columnas | Filas duplicadas exactas | Rango de fechas (`Date`) |
|---|---:|---:|---:|---|
| `xm_demanda.parquet` | 1.004 | 30 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_embalses.parquet` | 1.004 | 6 | 0 | 2024-01-01 a 2026-09-30 |
| `xm_precio_bolsa.parquet` | 1.004 | 30 | 0 | 2024-01-01 a 2026-09-30 |

## `xm_demanda.parquet`

`string` representa el tipo textual (`str`) detectado al leer el Parquet con
pandas. El porcentaje de nulos se calcula con `isna()` sobre cada columna.

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `string` | 0,0 % |
| `Id` | `string` | 0,0 % |
| `code` | `string` | 0,0 % |
| `Hour01` | `string` | 0,0 % |
| `Hour02` | `string` | 0,0 % |
| `Hour03` | `string` | 0,0 % |
| `Hour04` | `string` | 0,0 % |
| `Hour05` | `string` | 0,0 % |
| `Hour06` | `string` | 0,0 % |
| `Hour07` | `string` | 0,0 % |
| `Hour08` | `string` | 0,0 % |
| `Hour09` | `string` | 0,0 % |
| `Hour10` | `string` | 0,0 % |
| `Hour11` | `string` | 0,0 % |
| `Hour12` | `string` | 0,0 % |
| `Hour13` | `string` | 0,0 % |
| `Hour14` | `string` | 0,0 % |
| `Hour15` | `string` | 0,0 % |
| `Hour16` | `string` | 0,0 % |
| `Hour17` | `string` | 0,0 % |
| `Hour18` | `string` | 0,0 % |
| `Hour19` | `string` | 0,0 % |
| `Hour20` | `string` | 0,0 % |
| `Hour21` | `string` | 0,0 % |
| `Hour22` | `string` | 0,0 % |
| `Hour23` | `string` | 0,0 % |
| `Hour24` | `string` | 0,0 % |
| `_fuente` | `string` | 0,0 % |
| `_origen` | `string` | 0,0 % |
| `_extraido_en` | `string` | 0,0 % |

## `xm_embalses.parquet`

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `string` | 0,0 % |
| `Id` | `string` | 0,0 % |
| `Value` | `string` | 0,0 % |
| `_fuente` | `string` | 0,0 % |
| `_origen` | `string` | 0,0 % |
| `_extraido_en` | `string` | 0,0 % |

## `xm_precio_bolsa.parquet`

| Columna | Tipo de dato | Nulos |
|---|---|---:|
| `Date` | `string` | 0,0 % |
| `Id` | `string` | 0,0 % |
| `code` | `string` | 0,0 % |
| `Hour01` | `string` | 0,0 % |
| `Hour02` | `string` | 0,0 % |
| `Hour03` | `string` | 0,0 % |
| `Hour04` | `string` | 0,0 % |
| `Hour05` | `string` | 0,0 % |
| `Hour06` | `string` | 0,0 % |
| `Hour07` | `string` | 0,0 % |
| `Hour08` | `string` | 0,0 % |
| `Hour09` | `string` | 0,0 % |
| `Hour10` | `string` | 0,0 % |
| `Hour11` | `string` | 0,0 % |
| `Hour12` | `string` | 0,0 % |
| `Hour13` | `string` | 0,0 % |
| `Hour14` | `string` | 0,0 % |
| `Hour15` | `string` | 0,0 % |
| `Hour16` | `string` | 0,0 % |
| `Hour17` | `string` | 0,0 % |
| `Hour18` | `string` | 0,0 % |
| `Hour19` | `string` | 0,0 % |
| `Hour20` | `string` | 0,0 % |
| `Hour21` | `string` | 0,0 % |
| `Hour22` | `string` | 0,0 % |
| `Hour23` | `string` | 0,0 % |
| `Hour24` | `string` | 0,0 % |
| `_fuente` | `string` | 0,0 % |
| `_origen` | `string` | 0,0 % |
| `_extraido_en` | `string` | 0,0 % |

## Cómo repetir el perfilamiento

1. Ejecuta `python -m src.pipeline` para crear o actualizar los archivos de
   `data/bronze/`.
2. Lee cada Parquet con `pandas.read_parquet`.
3. Calcula filas y columnas con `df.shape`, los tipos con `df.dtypes`, y los
   nulos por columna con `df.isna().mean() * 100`.
4. Cuenta filas completamente duplicadas con `df.duplicated().sum()`.
5. Convierte `Date` a fecha y calcula su mínimo y máximo para informar el rango.
6. Actualiza este documento con los resultados del conjunto descargado.

Este perfilamiento incluye los archivos presentes durante la medición. Si el
pipeline descarga otras fuentes o archivos, agrégalos con el mismo formato.

## Hallazgos de calidad

Estos hallazgos se calcularon sobre los Parquet locales disponibles el
2026-10-24. La capa bronce conserva los datos sin limpiar; las correcciones y
normalizaciones deben realizarse en la capa plata.

| # | Hallazgo | Evidencia numérica | Recomendación |
|---:|---|---|---|
| 1 | Filas duplicadas en las ventas de EnerAndes. | Se detectaron **120 filas duplicadas exactas** en **4.184 filas**: 32 en 2023, 32 en 2024, 32 en 2025 y 24 en 2026 (**2,87 %** del total). | Revisar la clave de negocio y deduplicar en plata, conservando el registro válido. |
| 2 | Valores faltantes en campos de ventas de EnerAndes. | Los cuatro archivos suman **148 celdas nulas** en sus columnas de datos: 37 (2023), 28 (2024), 41 (2025) y 42 (2026). Los campos de linaje no presentan nulos. | Cuantificar nulos por campo y definir si se imputan, se excluyen o se conservan como desconocidos. |
| 3 | Esquema y filas de encabezado inconsistentes en EnerAndes. | Los **4 archivos anuales** exponen columnas genéricas `col_0`…; tres tienen 7 columnas de origen y uno 8. En 2023 y 2024 la primera fila contiene encabezados dentro de los datos; en 2025 y 2026 las primeras filas incluyen título y nota de fuente. | Normalizar nombres, unidades y formatos por año en plata; separar encabezados y metadatos antes de combinar. |
| 4 | Cobertura temporal incompleta en IDEAM. | Para el intervalo solicitado **2026-06-01 a 2026-09-30** hay **122 días**; el archivo contiene **52 fechas (42,62 %)** y faltan **70 (57,38 %)**. La fecha máxima es 2026-07-24; también faltan 2026-07-05 y 2026-07-06 dentro del tramo observado. | Revisar la extracción/paginación y la disponibilidad de la fuente; registrar explícitamente las fechas ausentes. |
| 5 | Conteos de observaciones IDEAM atípicamente altos. | De **2.784 registros estación-día**, **149 (5,35 %)** tienen `n_obs > 144`; dos registros del 2026-07-24 alcanzan **16.302** y **16.245**, mientras la mediana es **144**. | Validar la frecuencia esperada por estación y el agregado SoQL para descartar duplicación o diferencias de frecuencia. |

Los hallazgos 1–3 describen datos crudos de EnerAndes que requieren
estandarización; no implican que la capa bronce deba modificarse. El hallazgo 5
es una alerta para validar contra la frecuencia de medición de cada estación,
no una conclusión de que esos conteos sean necesariamente inválidos.
