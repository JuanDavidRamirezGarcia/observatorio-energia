# Bitácora de desarrollo y cambios — Capa Bronce

**Autor:** Juan David Ramírez García  
**Rama de trabajo:** `JuanDavidRamirezG-Data-Engineer`  
**Fase:** Extensión del pipeline de extracción y fuente propia (Capa Bronce)

## 1. Configuración del entorno y control de versiones

**Entorno de desarrollo:** Configuración y sincronización del entorno en GitHub Codespaces utilizando el entorno virtual `.venv` y las dependencias de `requirements.txt`.

**Gestión de ramas:** Creación y mantenimiento de la rama de trabajo `JuanDavidRamirezG-Data-Engineer`, realizando validaciones periódicas con `main` y revisión de *pull requests* para prevenir conflictos de integración.

## 2. Ampliación de la extracción de XM (API REST)

**Extensión del rango temporal:** Modificación de la configuración en `src/config.py` para ampliar la ventana de extracción histórica desde el `2024-01-01` hasta el `2026-09-30`.

**Incorporación de nuevas métricas:**

- **Gene:** Generación por planta (entidad Recurso, frecuencia horaria).
- **AporEner:** Aportes hídricos en energía (entidad Sistema, frecuencia diaria).
- **ListadoRecursos:** Catálogo general de plantas y recursos del sistema.

**Refactorización del extractor (`src/extract/xm.py`):**

- Extensión del código para soportar el endpoint `lists` (requerido por `ListadoRecursos`), el cual no acepta rango de fechas ni estructura por ventanas temporales.
- Modificación de la función `aplanar()` para procesar la clave `ListEntities` devuelta en la respuesta JSON del catálogo.

**Corrección de errores:** Ajuste del parámetro de fecha de inicio en `config.py` corrigiendo un desbordamiento de día (`FECHA_INICIO = date(2024, 1, 1)`).

## 3. Integración de fuente adicional propia (TRM)

**Selección de la fuente:** Integración de la Tasa Representativa del Mercado (TRM) obtenida desde la API REST SODA de Datos Abiertos Colombia / Banco de la República.

**Centralización de configuración:** Adición de la constante `TRM_URL` en `src/config.py`, con el valor [`https://www.datos.gov.co/resource/32sa-8pi3.json`](https://www.datos.gov.co/resource/32sa-8pi3.json).

**Creación del extractor (`src/extract/trm.py`):**

- Desarrollo del script de extracción automatizado con filtrado por rango de fechas (`vigenciadesde`).
- Guardado del resultado en formato Parquet en la ruta `data/bronze/trm_colombia.parquet` con sus respectivas columnas de linaje.

**Integración al pipeline (`src/pipeline.py`):**

- Importación del módulo `trm` y su inclusión dentro de la tupla de ejecución del pipeline principal.
- Actualización de la función `resumen()` para incluir la nueva tabla en el reporte de la terminal.

## 4. Documentación y calidad del proyecto

**Actualización del `README.md`:** Incorporación de la tabla de fuentes de la Capa Bronce, actualizando las métricas de XM y agregando el registro de la TRM, junto con la justificación de negocio (análisis de precios en USD y variaciones macroeconómicas).

**Pruebas de integración:** Verificación completa del pipeline mediante la ejecución del comando `python -m src.pipeline --forzar`, confirmando la creación e integridad de los archivos `.parquet`.

# Bitácora de desarrollo y cambios — Capa Oro (dbt)

**Autor:** Juan David Ramírez García  
**Rama de trabajo:** `juandavid-dbt-capa-oro`  
**Fase:** Modelado estrella, pruebas de calidad y linaje en la Capa Oro (dbt + DuckDB)

---

## 5. Implementación del Modelo Dimensional (Capa Oro con dbt)

### Configuración del entorno dbt y fuentes
- **Integración con DuckDB:** Configuración del adaptador `dbt-duckdb` en `profiles.yml` para conectarse a la base de datos `observatorio.duckdb` operando sobre los datos Parquet de la Capa Plata (`data/silver/`).
- **Estandarización de fuentes (`sources.yml`):** Mapeo de la fuente `silver` conectando la totalidad de los archivos Parquet procesados (`enerandes_ventas`, `enerandes_cuarentena`, `xm_precio_bolsa`, `xm_demanda`, `xm_embalses`, `noaa_oni`, `ideam_precipitacion`, `ideam_temperatura`).

### Construcción del Esquema Estrella (8 Tablas)
Se implementó un modelo estrella compuesto por 5 tablas de dimensión y 3 tablas de hechos:

- **Dimensiones:**
  - `dim_fecha`: Dimensión temporal diaria (2023–2026) con llaves numéricas en formato `YYYYMMDD`.
  - `dim_mes`: Dimensión agrupada a nivel mensual (`YYYY-MM`).
  - `dim_municipio`: Dimensión geográfica de municipios de Antioquia extraída de la fuente de ventas, asignando llaves primarias sustitutas (`municipio_id`).
  - `dim_segmento`: Dimensión de segmento de mercado y tipo de compra (`segmento_id`).
  - `dim_recurso`: Dimensión de recursos de generación energética a partir de las fuentes de embalses y demanda (`recurso_key`).

- **Tablas de Hechos:**
  - `fact_ventas_mensual`: Consolidado mensual de consumo en kWh, facturación en COP y total de clientes por municipio y segmento.
  - `fact_mercado_horario`: Registro horario del mercado mayorista integrando el precio de bolsa y la demanda total del sistema.
  - `fact_generacion_recurso`: Registro horario de generación energética por recurso vinculando la dimensión de fechas y recursos.

---

## 6. Depuración, Refactorización y Pruebas de Calidad

### Corrección de errores de compilación y referencias
- **Resolución de prefijos de fuentes:** Corrección global de llamadas `{{ source('plata', ...) }}` a `{{ source('silver', ...) }}` para asegurar el mapeo correcto en dbt.
- **Alineación de llaves primarias e interfaces:** Refactorización de joins entre tablas de hechos y dimensiones (reemplazo de uniones por campos textuales como `divipola` por llaves primarias numéricas `municipio_id`, `segmento_id` y `mes_id`).
- **Depuración de esquemas:** Limpieza de modelos en desarrollo (`fact_clima_diario` y `fact_operacion_diaria`) y unificación de nombres de columnas en la fuente (`temperatura_celsius` vs `temperatura_c`).

### Validación con `dbt build`
- **Definición de pruebas en `schema.yml`:** Configuración de pruebas automatizadas de integridad de datos:
  - Pruebas de unicitad (`unique`) y valores no nulos (`not_null`) en todas las llaves primarias de las dimensiones.
  - Pruebas de integridad referencial (`relationships`) entre las llaves foráneas de las tablas de hechos y sus respectivas dimensiones.
- **Resultado final:** Ejecución exitosa del comando `dbt build --project-dir dbt --profiles-dir dbt`, logrando un pase total de **35/35 nodos** (modelos de tablas, vistas y pruebas de calidad en verde sin errores ni advertencias).