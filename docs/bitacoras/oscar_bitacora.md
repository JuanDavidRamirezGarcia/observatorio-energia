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

## Capa Plata: puntos 1 y 2 — 2026-11-04

Se completó la limpieza de EnerAndes y de las demás fuentes solicitadas en los
puntos 1 y 2. El trabajo se concentró en `src/extract/`, `src/silver/`,
`src/config.py` y `src/transformar.py`.

### Punto 1: EnerAndes — cuatro hojas en una tabla plata

El archivo de bronce contiene una hoja por año, pero cada año tiene una
estructura diferente. La función `normalizar_encabezados()` busca la fila que
realmente contiene los nombres de negocio (`Fecha`, `Periodo`, `Mes`,
`Municipio` o `Ciudad`) y descarta automáticamente títulos y notas anteriores.
Esto permite procesar también las hojas 2025 y 2026, cuyo encabezado no está
en la primera fila.

Las reglas aplicadas son:

1. Se estandarizan los nombres de columnas a periodo, municipio, segmento,
   tipo de compra, energía, valor y clientes.
2. Se interpretan `YYYY-MM`, `mar-24`, `03/2024` y `01/03/2026`. La última
   fecha se procesa como día/mes/año, por lo que queda como `2026-03`.
3. Se reconocen abreviaturas de meses en español e inglés.
4. Se eliminan filas de totales del resultado analítico.
5. La energía se convierte por unidad: MWh se multiplica por 1.000 y kWh no
   se modifica.
6. Se normalizan municipios y alias como `Rio Negro`, `Rionegro (Ant)` y
   `Medellín D.E.` a su municipio y código DIVIPOLA.
7. Se normalizan segmentos y modalidades de compra.
8. Se convierten energía, valor y clientes a tipos numéricos.
9. Se eliminan duplicados corregibles después de normalizar las columnas.
10. Las filas que siguen siendo inválidas no se borran: se guardan en
    `data/silver/enerandes_cuarentena.parquet` con `motivo_cuarentena`.

Resultados verificados:

- `enerandes_ventas.parquet`: 4.007 filas limpias.
- `enerandes_cuarentena.parquet`: 45 filas con energía vacía/negativa,
  clientes inválidos u otros problemas no corregibles.

### Punto 2: XM — métricas horarias, diarias y catálogo

En `src/config.py` se configuraron las métricas `PrecBolsNaci`, `DemaReal`,
`Gene`, `AporEner`, `PorcVoluUtilDiar` y `ListadoRecursos`. Las métricas
temporales se descargan en ventanas de máximo 30 días porque ese es el límite
operativo de la API. El catálogo se consulta una sola vez mediante el endpoint
`lists`.

En `src/silver/xm.py`, `unpivot_24_horas()` convierte `Hour01` a `Hour24` en
filas con fecha, hora y valor numérico. Para generación la deduplicación usa
`code`, que identifica la planta; no se usa `Id` porque la API devuelve el
texto genérico `Recurso` para todas las plantas.

La generación fue procesada por bloques y escrita mediante PyArrow para evitar
cargar simultáneamente todas las filas horarias en memoria. Además, el
extractor guarda `Gene` de forma incremental después de cada ventana, de modo
que una interrupción no pierda todo el avance ya descargado.

Salidas verificadas:

- `xm_precio_bolsa.parquet`: 24.096 filas horarias.
- `xm_demanda.parquet`: 24.096 filas horarias.
- `xm_generacion.parquet`: 5.935.449 filas horarias, 633 códigos de planta,
  desde 2024-01-01 hasta 2026-09-30.
- `xm_embalses.parquet`: 1.004 registros diarios numéricos.
- `xm_aportes.parquet`: 1.004 registros diarios numéricos.
- `xm_listado_recursos.parquet`: 2.500 recursos normalizados.

### Punto 2: IDEAM

`src/silver/ideam.py` convierte la fecha a tipo fecha, transforma a número la
precipitación y las temperaturas media, mínima y máxima, conserva el código y
nombre de estación junto con el municipio y elimina duplicados por estación y
fecha.

También se corrigió la extracción para que el año 2025 se recorra completo:
`IDEAM_FECHA_INICIO` es `2025-01-01`, `IDEAM_FECHA_FIN` es `2025-12-31` y no
existe un límite artificial de diez ventanas.

Resultados: 2.374 registros de precipitación y 1.477 de temperatura.

### Punto 2: NOAA

`src/silver/noaa.py` asigna cada trimestre móvil a su mes central: `DJF` a
enero, `JFM` a febrero, y así sucesivamente hasta `NDJ` a diciembre. El ONI se
convierte a número y se clasifica así:

- `ONI >= 0.5`: `El Niño`.
- `ONI <= -0.5`: `La Niña`.
- En los demás casos: `Neutral`.

El resultado es `data/silver/noaa_oni.parquet`, con 920 registros mensuales.

### Punto 2: fuente propia TRM

Se creó `src/silver/trm.py`. La fecha `vigenciadesde` se convierte a fecha, el
valor TRM se convierte a número, se eliminan duplicados por día y se ordena
cronológicamente. El resultado es `data/silver/trm_colombia.parquet`, con 649
registros.

### Reproducción de los puntos 1 y 2

Desde la raíz del repositorio:

```bash
python -m src.pipeline --forzar       # solo si se necesitan descargar datos nuevos
python -m src.transformar            # construye las salidas de Capa Plata
python -m pytest -q                  # valida las pruebas existentes
```

La extracción XM puede tardar por la cantidad de plantas y ventanas. Si solo
se necesita reconstruir plata con los archivos ya descargados, se ejecuta
únicamente `python -m src.transformar`.

La verificación final registró 19 pruebas aprobadas. Los archivos Parquet de
`data/silver/` no se versionan; cada integrante debe generarlos localmente
cuando los necesite. Esta bitácora documenta únicamente los puntos 1 y 2.
