# Reporte de calidad de datos

## Alcance y lectura de las métricas

Este corte compara los archivos Parquet disponibles en `data/bronze/` y
`data/silver/` con las reglas implementadas en `src/silver/`. Las cifras son
conteos de filas o valores en esos archivos; pueden cambiar al ejecutar de
nuevo el pipeline con datos más recientes. En las métricas de EnerAndes,
“candidatas” son las filas de datos una vez retirados los encabezados,
metadatos y totales de las cuatro hojas.

## EnerAndes

Se procesaron las hojas 2023–2026 del archivo de ventas. La salida contiene
4.007 filas en `data/silver/enerandes_ventas.parquet`; otras 45 filas quedaron
en `data/silver/enerandes_cuarentena.parquet`.

| Problema o control | Regla aplicada | Antes | Después |
|---|---|---:|---:|
| Encabezados y filas de total mezclados con los datos | Detectar y estandarizar encabezados; retirar metadatos/encabezados y las filas `TOTAL` | 4.184 filas de bronce | 4.170 filas candidatas (10 encabezados/metadatos y 4 totales excluidos) |
| Fechas y periodos en formatos distintos | Estandarizar el periodo a `AAAA-MM` | 4.170 periodos candidatos | 4.170 periodos interpretables |
| Energía reportada en MWh | Convertir a kWh multiplicando por 1.000 | 347 filas con unidad MWh | 345 convertidas a kWh; 1 con energía vacía/no numérica y 1 negativa quedaron en cuarentena |
| Fecha inválida o vacía | Enviar a cuarentena si el periodo no se puede interpretar | 0 filas inválidas | 0 filas en cuarentena por fecha |
| Energía inválida o vacía | Convertir a número; enviar a cuarentena si queda nula | 27 filas inválidas/vacías | 0 en plata; 27 en cuarentena |
| Energía negativa | Enviar a cuarentena cuando `energia_kwh < 0` | 18 filas negativas | 0 en plata; 18 en cuarentena |
| Valor facturado negativo | Enviar a cuarentena cuando `valor_cop < 0` | 0 filas negativas | 0 filas en cuarentena por este motivo |
| Municipio vacío o no reconocido | Normalizar nombre y validar correspondencia DIVIPOLA; enviar fallos a cuarentena | 0 municipios inválidos | 0 filas en cuarentena por este motivo |
| Clientes inválidos o vacíos | Convertir a entero y enviar valores nulos a cuarentena | 0 filas inválidas/vacías | 0 filas en cuarentena por este motivo |
| Filas repetidas entre los registros válidos | Eliminar duplicados en la salida unificada | 4.125 filas válidas antes de deduplicar | 4.007 filas en plata; 118 repeticiones válidas removidas y 0 duplicados en plata |

### Cuarentena EnerAndes

| Motivo registrado | Filas |
|---|---:|
| Energía inválida o vacía | 27 |
| Energía negativa | 18 |
| **Total en cuarentena** | **45** |

Los seis tipos de error contemplados por la regla de cuarentena son fecha
inválida/vacía, energía inválida/vacía, energía negativa, valor facturado
negativo, municipio inválido/vacío y clientes inválidos/vacíos. En este corte
solo se registraron los dos motivos con filas en la tabla. La comparación
válida para la energía es estrictamente `< 0` (no `<= 0`).

## XM

| Problema o control | Regla aplicada | Antes | Después |
|---|---|---:|---:|
| Precio en 24 columnas horarias | Despivotar `Hour01`–`Hour24` a una fila por fecha y hora | 1.004 filas diarias × 24 horas | 24.096 filas horarias en `xm_precio_bolsa.parquet` |
| Demanda en 24 columnas horarias | Despivotar `Hour01`–`Hour24` a una fila por fecha y hora | 1.004 filas diarias × 24 horas | 24.096 filas horarias en `xm_demanda.parquet` |
| Generación horaria dispersa | Despivotar las 24 horas y descartar valores nulos o fechas inválidas | 8.408.664 celdas horarias potenciales; 2.473.215 nulas | 5.935.449 filas horarias válidas en `xm_generacion.parquet` |
| Claves repetidas en precio, demanda y generación | Deduplicar por fecha, hora y código/identificador de recurso | 0 duplicados por llave en las salidas medidas | 0 duplicados por llave |
| Fechas o valores inválidos en embalses | Convertir fecha/valor; descartar nulos y duplicados por fecha e identificador | 1.004 filas; 0 fechas/valores inválidos | 1.004 filas en `xm_embalses.parquet` |
| Fechas o valores inválidos en aportes | Convertir fecha/valor; descartar nulos y duplicados por fecha e identificador | 1.004 filas; 0 fechas/valores inválidos | 1.004 filas en `xm_aportes.parquet` |
| Registros repetidos en ListadoRecursos | Normalizar el objeto `Values` y eliminar filas repetidas | 2.502 registros; 2 repetidos | 2.500 filas en `xm_listado_recursos.parquet`; 0 filas idénticas repetidas |

## IDEAM

| Problema o control | Regla aplicada | Antes | Después |
|---|---|---:|---:|
| Fechas, valores y llave estación-fecha de precipitación | Convertir fecha y precipitación a tipos válidos; retirar nulos y duplicados por estación-fecha | 2.374 filas; 0 fechas/valores inválidos y 0 llaves repetidas | 2.374 filas en `ideam_precipitacion.parquet` |
| Fechas, valores y llave estación-fecha de temperatura | Convertir fecha y variables a tipos válidos; admitir coma decimal; retirar nulos y duplicados por estación-fecha | 1.477 filas; 0 fechas/valores inválidos y 0 llaves repetidas | 1.477 filas en `ideam_temperatura.parquet` |
| Formato decimal en temperatura | Reemplazar coma por punto antes de convertir a número | 0 valores con coma en las columnas medidas | 0 valores inválidos después de la conversión |

## NOAA (ONI)

| Problema o control | Regla aplicada | Antes | Después |
|---|---|---:|---:|
| Trimestre móvil no reconocido | Mapear `SEAS` a mes y retirar periodos nulos | 920 periodos; 0 temporadas inválidas | 920 periodos interpretables |
| Anomalía ONI no numérica | Convertir `ANOM` a número y retirar valores nulos | 920 valores; 0 inválidos | 920 valores válidos en `noaa_oni.parquet` |
| Clasificación de fase ENSO | Clasificar ONI con umbrales `>= 0,5` (El Niño) y `<= -0,5` (La Niña) | 920 valores ONI | 234 El Niño, 238 La Niña y 448 Neutral |

## TRM

| Problema o control | Regla aplicada | Antes | Después |
|---|---|---:|---:|
| Fecha de vigencia inválida | Convertir fecha y retirar registros sin fecha | 649 filas; 0 fechas inválidas | 649 filas con fecha |
| TRM no numérica | Reemplazar coma decimal por punto, convertir a número y retirar nulos | 649 filas; 0 valores inválidos | 649 valores válidos en `trm_colombia.parquet` |
| Fechas repetidas | Deduplicar por fecha | 0 fechas repetidas | 0 fechas repetidas |

## Resumen

- Filas de EnerAndes en plata: **4.007**.
- Filas de EnerAndes en cuarentena: **45** (27 por energía inválida/vacía y
  18 por energía negativa).
- El resto de los controles enumerados no encontró filas inválidas en los
  archivos de este corte; sus métricas se muestran como `0 → 0` o como filas
  conservadas sin pérdida.
