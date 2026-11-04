# Diccionario de datos de la capa oro

Este documento describe la estructura de las tablas del modelo dimensional de la capa oro para el Observatorio Energía y Clima. Su propósito es facilitar el entendimiento del grano de negocio, las claves de unión y el origen de cada columna en el modelo analítico.

## 1. Convenciones

- Las tablas de dimensión (`dim_*`) contienen atributos descriptivos y catalogados.
- Las tablas de hechos (`fact_*`) contienen métricas medibles y se agrupan según un grano específico.
- Las columnas con sufijo `_id` representan llaves foráneas a las dimensiones.
- Los tipos de dato se expresan como convenciones analíticas y pueden materializarse según el motor final (DuckDB, PostgreSQL o Spark).

## 2. Grano de las tablas de hechos

### `fact_ventas_mensual`
Un registro por cada periodo (`YYYY-MM`), municipio, segmento de cliente y tipo de compra (`Bolsa` / `Contrato`).

Esto permite responder preguntas como:
- ¿Cuánto se vendió por municipio cada mes?
- ¿Cómo cambia el volumen por tipo de compra?
- ¿Qué segmento comercial lidera la venta en cada periodo?

### `fact_mercado_horario`
Un registro por fecha y hora, consolidando el precio de bolsa y la demanda
total horaria del sistema.

Esto permite responder preguntas como:
- ¿Cuál fue el precio promedio del mercado en cada hora?
- ¿Cuándo aumenta la demanda del sistema?
- ¿Existe relación entre demanda y precio por franja horaria?

### `fact_generacion_recurso`
Un registro por fecha, hora y planta (código de recurso), con generación medida
en MWh.

Esto permite responder preguntas como:
- ¿Qué recurso genera más energía en cada hora?
- ¿Cómo cambia la mezcla de generación a lo largo del día?
- ¿Qué tecnologías presentan mayor variabilidad en el tiempo?

## 3. Diccionario por tabla

### Tabla: `dim_fecha`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `fecha_key` | BIGINT / INT | Llave primaria sintética del calendario | Derived (`dim_fecha`) |
| `fecha` | DATE | Fecha del registro | `silver.xm_*`, `silver.ideam_*`, `silver.noaa_*`, `silver.trm_*` |
| `anio` | INT | Año calendario | Derived from `fecha` |
| `mes` | INT | Mes del año (1-12) | Derived from `fecha` |
| `nombre_mes` | VARCHAR | Nombre del mes | Derived from `fecha` |
| `dia` | INT | Día del mes | Derived from `fecha` |
| `trimestre` | INT | Trimestre del año (1-4) | Derived from `fecha` |
| `nombre_dia` | VARCHAR | Nombre del día de la semana | Derived from `fecha` |
| `es_fin_de_semana` | BOOLEAN | Indica si la fecha corresponde a fin de semana | Derived from `fecha` |

### Tabla: `dim_mes`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `mes_id` | BIGINT / INT | Llave primaria sintética del periodo mensual | Derived (`dim_mes`) |
| `periodo` | VARCHAR | Periodo mensual en formato `YYYY-MM` | `silver.enerandes_ventas` |
| `anio` | INT | Año del periodo | Derived from `periodo` |
| `mes` | INT | Número del mes | Derived from `periodo` |
| `nombre_mes` | VARCHAR | Nombre del mes | Derived from `periodo` |
| `trimestre` | INT | Trimestre al que pertenece el mes | Derived from `periodo` |

### Tabla: `dim_municipio`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `municipio_id` | BIGINT / INT | Llave primaria de municipio | Derived (`dim_municipio`) |
| `municipio` | VARCHAR | Nombre del municipio | `silver.enerandes_ventas` |
| `departamento` | VARCHAR | Departamento del municipio | `silver.enerandes_ventas` |
| `region` | VARCHAR | Región geográfica | `silver.enerandes_ventas` |
| `zona` | VARCHAR | Zona o subregión de análisis | `silver.enerandes_ventas` |

### Tabla: `dim_segmento`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `segmento_id` | BIGINT / INT | Llave primaria del segmento | Derived (`dim_segmento`) |
| `segmento` | VARCHAR | Nombre del segmento de cliente | `silver.enerandes_ventas` |
| `categoria` | VARCHAR | Categoría del segmento | `silver.enerandes_ventas` |
| `descripcion` | VARCHAR | Descripción funcional del segmento | `silver.enerandes_ventas` |

### Tabla: `dim_recurso`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `recurso_key` | BIGINT / INT | Llave primaria del recurso | Derived (`dim_recurso`) |
| `codigo_recurso` | VARCHAR | Código XM de la planta | `silver.xm_listado_recursos` |
| `nombre_recurso` | VARCHAR | Nombre del recurso | `silver.xm_listado_recursos` |
| `tipo_generacion` | VARCHAR | Tipo de generación reportado por XM | `silver.xm_listado_recursos` |
| `fuente_energia` | VARCHAR | Fuente de energía reportada por XM | `silver.xm_listado_recursos` |
| `empresa` | VARCHAR | Código de empresa reportado por XM | `silver.xm_listado_recursos` |
| `disponibilidad` | VARCHAR | Clasificación de despacho reportada por XM | `silver.xm_listado_recursos` |
| `estado` | VARCHAR | Estado operativo reportado por XM | `silver.xm_listado_recursos` |

### Tabla: `fact_ventas_mensual`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `mes_id` | BIGINT / INT | Llave foránea a `dim_mes` | Derived (`dim_mes`) |
| `municipio_id` | BIGINT / INT | Llave foránea a `dim_municipio` | Derived (`dim_municipio`) |
| `segmento_id` | BIGINT / INT | Llave foránea a `dim_segmento` | Derived (`dim_segmento`) |
| `periodo` | VARCHAR | Periodo comercial en formato `YYYY-MM` | `silver.enerandes_ventas` |
| `tipo_compra` | VARCHAR | Modalidad de compra: `Bolsa` / `Contrato` | `silver.enerandes_ventas` |
| `energia_kwh` | DOUBLE | Energía vendida en kWh | `silver.enerandes_ventas` |
| `valor_cop` | DOUBLE | Valor comercial de la venta en COP | `silver.enerandes_ventas` |
| `clientes` | BIGINT / INT | Cantidad de clientes asociados al registro | `silver.enerandes_ventas` |
| `fuente` | VARCHAR | Nombre de la fuente de origen | `silver.enerandes_ventas` |

### Tabla: `fact_mercado_horario`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `fecha_key` | BIGINT / INT | Llave foránea a `dim_fecha` | Derived (`dim_fecha`) |
| `fecha` | DATE | Fecha del dato horario | `silver.xm_precio_bolsa`, `silver.xm_demanda` |
| `hora` | INT | Hora del día (1-24, como reporta XM) | `silver.xm_precio_bolsa`, `silver.xm_demanda` |
| `precio_bolsa_kwh` | DOUBLE | Precio horario del mercado en COP/kWh | `silver.xm_precio_bolsa` |
| `demanda_kwh` | DOUBLE | Demanda total horaria del sistema | `silver.xm_demanda` |

### Tabla: `fact_generacion_recurso`
| Columna | Tipo de Dato | Descripción | Origen / Fuente |
| :--- | :--- | :--- | :--- |
| `fecha_key` | BIGINT / INT | Llave foránea a `dim_fecha` | Derived (`dim_fecha`) |
| `recurso_key` | BIGINT / INT | Llave foránea a `dim_recurso` | Derived (`dim_recurso`) |
| `fecha` | DATE | Fecha de generación | `silver.xm_generacion` |
| `hora` | INT | Hora de generación (1-24, como reporta XM) | `silver.xm_generacion` |
| `codigo_recurso` | VARCHAR | Código XM de la planta | `silver.xm_listado_recursos` |
| `generacion_mwh` | DOUBLE | Energía generada en MWh | `silver.xm_generacion` |

## 4. Observaciones de diseño

- `fact_ventas_mensual` es una tabla de agregación mensual, por lo que su grano es más bajo en granularidad que el de mercado horario o generación por hora.
- `fact_mercado_horario` centraliza la señal del mercado eléctrico y permite análisis de volatilidad, picos y patrones diurnos.
- `fact_generacion_recurso` es clave para análisis de mezcla energética y diagnóstico de generación por tecnología.
- Las dimensiones (`dim_*`) no contienen hechos; solo describen contexto y permiten filtros analíticos, segmentación y joins de negocio.

## 5. Recomendación de uso

Para análisis de BI y dashboards, la combinación recomendada es:

- `fact_ventas_mensual` + `dim_mes` + `dim_municipio` + `dim_segmento`
- `fact_mercado_horario` + `dim_fecha` + `dim_hora` + `dim_mercado`
- `fact_generacion_recurso` + `dim_fecha` + `dim_hora` + `dim_recurso`

Esto asegura un modelo consistente, fácil de consultar y compatible con dashboards y consultas analíticas.
