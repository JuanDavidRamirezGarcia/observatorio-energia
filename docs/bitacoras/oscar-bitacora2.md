# Bitácora de actividades — Observatorio de Energía

**Proyecto:** Observatorio de Energía (`observatorio-energia`)

**Rol:** BI Analyst / Data Engineer

**Rama de trabajo:** `feature/plata-oro`

## 1. Actividad previa: extracción de datos IDEAM

### Objetivo

Ampliar la extracción de datos abiertos del IDEAM mediante Socrata / SoQL
para monitorear precipitación e incorporar variables de temperatura del aire,
procesando y filtrando los datos directamente en el servidor.

### Tareas realizadas

- Ajuste del rango temporal desde el 1 de enero de 2025.
- Filtrado geográfico por departamento y por intervalo de fechas mediante
  SoQL.
- Agregación diaria por estación de precipitación, con acumulación total y
  conteo de observaciones.
- Incorporación del dataset de temperatura del aire `sbwg-7ju4`.
- Implementación de agregaciones diarias de temperatura media, mínima y
  máxima.
- Reutilización de la lógica `_extraer_dataset_ideam` para ventanas semanales.
- Uso de `date_trunc_ymd(fechaobservacion)` para reducir la transferencia de
  datos y limitar la extracción a un máximo de 10 ventanas.
- Generación de muestras CSV de 50 registros.

### Verificación

```bash
python -m src.extract.ideam --forzar
```

Se confirmó la generación de muestras con 50 registros mediante inspección en
Python y comandos de terminal.

## 2. Actividad actual: implementación y documentación de la Capa Plata

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
  sección “Uso de IA” en [`README.md`](README.md).
- Documentación de la rama `feature/plata-oro`, el alcance de los puntos 1 al
  4 y el entorno de ejecución con Python 3.10+, Pandas, Pandera y Pytest en
  [`README.md`](../../README.md).
- Registro de los archivos Parquet generados en `data/silver/`, sus cantidades
  de registros y las reglas aplicadas a EnerAndes, XM, NOAA e IDEAM.
- Documentación del comando de transformación:

  ```bash
  python -m src.transformar
  ```

- Inclusión de los archivos de salida disponibles para la integración con la
  Capa Oro mediante dbt y DuckDB.

## 3. Cambios nuevos detectados en el repositorio

Durante la revisión posterior de la rama se identificaron cambios adicionales
relacionados con la integración:

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
