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
