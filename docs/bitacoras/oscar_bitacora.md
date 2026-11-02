# Bitácora de actividades — Extracción de datos IDEAM

**Proyecto:** Observatorio de Energía (`observatorio-energia`)

**Rol:** BI Analyst / Data Engineer

**Rama de trabajo:** `oscar-BI-Analyst`

**Módulo modificado:** [`src/extract/ideam.py`](../../src/extract/ideam.py)

## 1. Objetivo de la actividad

Ampliar la capacidad de extracción de la fuente de datos abiertos del IDEAM
(plataforma Socrata / SoQL) para el monitoreo de precipitación e incorporar
variables de temperatura del aire, garantizando el procesamiento y filtrado
directamente en el servidor.

## 2. Tareas realizadas

### A. Desarrollo e implementación en código

#### Ampliación de precipitación

- Ajuste del rango temporal desde el 1 de enero de 2025 (`2025-01-01`).
- Filtrado geográfico por departamento (`config.IDEAM_DEPARTAMENTO`) e
  intervalo de fechas en el servidor mediante SoQL.
- Agregación diaria por estación, calculando:
  - La acumulación total de lluvias (`sum(valorobservado)`).
  - El conteo de observaciones.

#### Inclusión del dataset de temperatura del aire

- Incorporación del dataset `sbwg-7ju4`.
- Configuración del endpoint:
  [`https://www.datos.gov.co/resource/sbwg-7ju4.json`](https://www.datos.gov.co/resource/sbwg-7ju4.json).
- Implementación de la función `consulta_soql_temperatura` para calcular
  agregaciones diarias por estación:
  - **Temperatura media:** `avg(valorobservado)`.
  - **Temperatura mínima:** `min(valorobservado)`.
  - **Temperatura máxima:** `max(valorobservado)`.

#### Optimización de consultas SoQL y paginación

- Reutilización de la lógica modular `_extraer_dataset_ideam` para procesar
  ventanas de tiempo semanales.
- Agregación nativa con `date_trunc_ymd(fechaobservacion)` para reducir el
  consumo de ancho de banda y evitar la descarga de millones de filas no
  agregadas a Python.
- Control de iteraciones, acotando la extracción a un máximo de 10 ventanas
  semanales para optimizar el tiempo de ejecución.
- Generación automática de muestras de 50 registros en formato CSV mediante
  `df.head(50)`.

### B. Gestión de control de versiones

#### Creación y renombrado de rama

- Creación de la rama de trabajo local `oscargarcia-BI-Analyst`.
- Sincronización y renombrado posterior a `oscar-BI-Analyst` para coincidir con
  la rama remota en GitHub.

#### Resolución de conflictos de divergencia

- Reconciliación de cambios con la rama principal mediante:

  ```bash
  git pull origin main
  ```

- Enlace del canal de rastreo remoto (*upstream*) mediante:

  ```bash
  git branch --set-upstream-to=origin/oscar-BI-Analyst
  ```

#### Publicación de cambios

- Envío de las confirmaciones (*commits*) a la rama remota
  `origin/oscar-BI-Analyst`.

## 3. Entregables generados

| Entregable | Ubicación / referencia | Descripción |
|---|---|---|
| Script extractor | [`src/extract/ideam.py`](../../src/extract/ideam.py) | Código Python optimizado con SoQL para precipitación y temperatura. |
| Muestra de precipitación | [`data/samples/ideam_precipitacion_diaria_sample.csv`](../../data/samples/ideam_precipitacion_diaria_sample.csv) | Archivo de prueba con 50 registros agregados por día y estación. |
| Muestra de temperatura | [`data/samples/ideam_temperatura_diaria_sample.csv`](../../data/samples/ideam_temperatura_diaria_sample.csv) | Archivo de prueba con métricas diarias: media, mínima y máxima. |
| Rama remota | `origin/oscar-BI-Analyst` | Rama publicada en el repositorio central de GitHub. |

## 4. Pruebas de verificación

- Ejecución en terminal:

  ```bash
  python -m src.extract.ideam --forzar
  ```

- Conteo de registros: confirmado mediante inspección en Python
  (`len(df) == 50`) y comandos de terminal.

## Capa Plata

### Objetivo

Construir y documentar la entrega de la Capa Plata (Evidencia 2), aplicando
limpieza, tipado, deduplicación y validación de calidad a los datos de
EnerAndes, XM, NOAA e IDEAM, y dejando los resultados listos para la Capa
Oro.

### Tareas realizadas

- Implementación de los módulos de limpieza en `src/silver/`:
  `enerandes.py`, `xm.py`, `noaa.py` e `ideam.py`.
- Normalización de ventas de EnerAndes de 2023 a 2026, conversión de MWh a
  kWh, eliminación de duplicados y separación de registros inválidos en
  cuarentena.
- Transformación de las columnas horarias de XM a formato vertical para
  precios y demanda, además de la limpieza de embalses.
- Transformación del índice ONI de NOAA a meses, cálculo de anomalías y
  clasificación de las fases ENSO.
- Limpieza de fechas y valores numéricos de IDEAM, incluida la conversión de
  comas decimales en las temperaturas.
- Definición de contratos de calidad con Pandera en
  `src/quality/esquemas.py`, validando tipos, llaves, rangos y valores nulos.
- Creación del orquestador `src/transformar.py` para ejecutar la limpieza de
  las cuatro fuentes y generar archivos Parquet en `data/silver/`.
- Generación de los archivos `data/silver/enerandes_ventas.parquet`,
  `enerandes_cuarentena.parquet`, `xm_precio_bolsa.parquet`,
  `xm_demanda.parquet`, `xm_embalses.parquet`, `noaa_oni.parquet`,
  `ideam_precipitacion.parquet` e `ideam_temperatura.parquet`.
- Adición de pruebas automatizadas en `tests/test_limpieza.py`; la suite
  documentada para esta entrega registró 13 pruebas aprobadas.
- Incorporación de una sección independiente de Capa Plata después de la
  sección “Uso de IA” en `README.md`.
- Documentación de la rama `feature/plata-oro`, el alcance de los puntos 1 al
  4 y el entorno de ejecución con Python 3.10+, Pandas, Pandera y Pytest en
  `README.md`.
- Registro de los archivos Parquet generados en `data/silver/`, sus cantidades
  de registros y las reglas aplicadas a EnerAndes, XM, NOAA e IDEAM.
- Documentación del comando de transformación:

  ```bash
  python -m src.transformar
  ```

- Inclusión de los archivos de salida disponibles para la integración con la
  Capa Oro mediante dbt y DuckDB.

### Cambios adicionales relacionados con la integración

- Adición de `pandera` y `dbt-duckdb` en `requirements.txt`.
- Incorporación de `DIR_SILVER` y `DIR_DOCS` en `src/config.py`.
- Actualización de `.gitignore` para excluir los Parquet de Plata, archivos
  DuckDB, artefactos de dbt y la caché de Pytest.
- Regeneración de muestras CSV en `data/sample/`.
- Creación de una estructura preliminar de dbt en `dbt/`, con archivos para
  staging, dimensiones, hechos, fuentes y perfiles.
- Creación de `logs/dbt.log` como evidencia de ejecución.

La estructura de dbt todavía no constituye una Capa Oro funcional: los
archivos `dbt_project.yml`, `profiles.yml`, los modelos SQL y `schema.yml`
están vacíos. El intento registrado en el log terminó con el error
`dbt_project.yml does not parse to a dictionary`; por ello, queda pendiente
completar la configuración, los modelos y las pruebas de dbt antes de afirmar
que la Capa Oro está terminada.

### Verificación de la Capa Plata

```bash
python -m src.transformar
python -m pytest -v
git diff --check
```

La ejecución histórica documentada registró 13 pruebas aprobadas y la
validación de formato del README se completó sin errores. En la revisión
actual, el entorno utilizado no tenía instalados `pytest` ni el comando
`dbt`, por lo que esas dos verificaciones deben repetirse después de instalar
las dependencias declaradas.
