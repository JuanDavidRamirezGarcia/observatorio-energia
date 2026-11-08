# Observatorio Energía y Clima – Equipo <nombre>

> Proyecto Integrado IV – Integración de Información · IU Digital de Antioquia · 2026-2

## 👥 Integrantes

| Nombre | Usuario GitHub | Rol |
|---|---|---|
| juan david ramirez | Líder técnico | Data Engineer |
| rober castillo| Data Quality | Analyst |
| Juan Fernando Cataño Higuita|juancatano-col | Analytics Engineer |
| oscar garcia garcia| BI Analyst | Storyteller |

## 🎯 Objetivo

Integrar datos del mercado eléctrico (XM), del clima (IDEAM y NOAA) y de ventas internas (EnerAndes) para analizar el riesgo energético de Colombia ante El Niño 2026.

## 📦 Fuentes de datos (capa bronce)

El pipeline conserva los datos extraídos en formato Parquet e incluye columnas
de linaje (`_fuente`, `_origen` y `_extraido_en`). Las fuentes y sus archivos
de salida son:

| Fuente | Origen y método de extracción | Datos | Archivos Parquet en `data/bronze/` |
|---|---|---|---|
| XM – API Sinergox | API REST, respuestas JSON | Precio, demanda, generación, aportes, embalses y catálogo de plantas | `xm_precio_bolsa.parquet`, `xm_demanda.parquet`, `xm_generacion.parquet`, `xm_aportes.parquet`, `xm_embalses.parquet`, `xm_listado_recursos.parquet` |
| IDEAM – datos.gov.co | API Socrata, consultas SoQL | Precipitación diaria y temperatura diaria por estación en Antioquia | `ideam_precipitacion_diaria.parquet`, `ideam_temperatura_diaria.parquet` |
| NOAA – índice ONI | Archivo de texto descargado y tabulado | Índice Oceanic Niño (ONI) | `noaa_oni.parquet` |
| EnerAndes | Excel interno (`data/insumos/ventas_enerandes_2023_2026.xlsx`) | Ventas anuales 2023–2026, una hoja por año | `enerandes_ventas_2023.parquet`, `enerandes_ventas_2024.parquet`, `enerandes_ventas_2025.parquet`, `enerandes_ventas_2026.parquet` |
| TRM – Banco de la República, Datos Abiertos Colombia | API Socrata, solicitud GET con respuesta JSON | Tasa Representativa del Mercado para el rango configurado | `trm_colombia.parquet` |

## Fuente Adicional Propia

* **Nombre:** Tasa Representativa del Mercado (TRM).
* **Origen:** Banco de la República vía Portal de Datos Abiertos de Colombia (`https://www.datos.gov.co/d/32sa-8pi3`).
* **Uso y Propósito:**
Nos permite convertir los precios spot del mercado eléctrico (COP/MWh) y las ventas de energía a USD, facilitando el análisis de correlación entre la Tasa de Cambio y las variaciones en los precios de energía durante el periodo estudiado.

## ⚙️ Cómo ejecutar

Requisitos: Python 3.10 o posterior y acceso a Internet para consultar las
fuentes públicas. El archivo interno
`data/insumos/ventas_enerandes_2023_2026.xlsx` está incluido en el repositorio;
no es necesario copiarlo aparte.

Desde la raíz del proyecto, crea el entorno e instala las dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.pipeline
.\.venv\Scripts\python.exe -m src.consultar
.\.venv\Scripts\python.exe -m pytest
```

En macOS o Linux, usa el intérprete del entorno virtual con estos comandos:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.pipeline
.venv/bin/python -m src.consultar
.venv/bin/python -m pytest
```

El pipeline descarga XM, IDEAM, NOAA y TRM, y lee el Excel de EnerAndes.
Necesita conexión a Internet y el tiempo total depende de la disponibilidad
de las API; la generación horaria de XM puede tardar varios minutos. Al
terminar, genera en `data/sample/` un CSV por cada Parquet de bronce encontrado,
con sus primeras 200 filas (o todas si contiene menos). Los CSV de muestra se
versionan; `data/bronze/` contiene datos descargados y está excluida de Git.

Para volver a descargar todo: `python -m src.pipeline --forzar`. El rango de fechas se cambia en `src/config.py`.

## 🏗️ Arquitectura

```
Fuentes -> BRONCE (dato tal cual + linaje) -> PLATA (limpio) -> ORO (modelo estrella) -> Dashboard
```

## 📊 Resultados de consultas de la capa oro

Las consultas de negocio se almacenan en `consultas/oro/` y fueron ejecutadas en DuckDB sobre datos derivados del modelo analítico.

### 1) Municipios con mayor consumo en kWh

| Municipio | Consumo (GWh) |
|---|---:|
| Medellín | 16572.49 |
| Bello | 3929.85 |
| Itagüí | 2946.06 |
| Envigado | 2632.21 |
| Rionegro | 1910.89 |
| Sabaneta | 1644.75 |
| Apartadó | 1328.41 |
| Turbo | 1113.57 |
| Copacabana | 954.87 |
| La Estrella | 940.26 |

### 2) Promedio de precio de bolsa por hora y fase ENSO

| Hora | Fase ENSO | Precio promedio (COP/kWh) |
|---:|---|---:|
| 0 | El Niño | 437.58 |
| 1 | El Niño | 437.16 |
| 2 | El Niño | 435.89 |
| 3 | El Niño | 434.64 |
| 4 | El Niño | 439.70 |
| 5 | El Niño | 452.04 |
| 6 | El Niño | 441.29 |
| 7 | El Niño | 413.96 |
| 8 | El Niño | 395.21 |
| 9 | El Niño | 387.64 |

### 3) Comparativo horario de generación vs demanda

| Hora | Generación (MWh) | Demanda (MWh) | Diferencia (MWh) |
|---:|---:|---:|---:|
| 0 | 8,712,276.21 | 8,712,276.21 | 0.00 |
| 1 | 8,416,696.11 | 8,416,696.11 | 0.00 |
| 2 | 8,200,508.65 | 8,200,508.65 | 0.00 |
| 3 | 8,082,390.33 | 8,082,390.33 | 0.00 |
| 4 | 8,169,164.38 | 8,169,164.38 | 0.00 |
| 5 | 8,396,448.57 | 8,396,448.57 | 0.00 |
| 6 | 8,495,008.73 | 8,495,008.73 | 0.00 |
| 7 | 8,905,922.19 | 8,905,922.19 | 0.00 |
| 8 | 9,341,290.77 | 9,341,290.77 | 0.00 |
| 9 | 9,634,153.22 | 9,634,153.22 | 0.00 |

## 🎥 **Videos Explicativos del Equipo**

Enlace a los videos: [Ver Videos](https://drive.google.com/drive/folders/1zofZjFRxsIK27Ge3yDA0Vbg2BPMILYhW?usp=drive_link)

## Evidencias de ejecución de consola

**Ejecución del Pipeline Bronce**

<img width="876" height="500" alt="image" src="https://github.com/user-attachments/assets/3d4df93a-8883-4e32-8f28-9401c37f3e7e" />
<img width="876" height="500" alt="image" src="https://github.com/user-attachments/assets/8037d274-0bf6-4341-beea-1f8c463decb3" />

**Pruebas Automatizadas (Pytest)**

<img width="857" height="381" alt="image" src="https://github.com/user-attachments/assets/c4316a7a-a6f0-495b-9001-34bd56e0c8e6" />




## 🤖 Uso de IA

Durante el desarrollo del proyecto se utilizaron herramientas de inteligencia
artificial como apoyo:

- **Gemini:** apoyo para consultar conceptos y comprender las fuentes de datos
  utilizadas en el proyecto.
- **GitHub Copilot:** apoyo para organizar y estructurar el código.

Las respuestas y sugerencias se revisaron y validaron por el equipo antes de
incorporarlas al proyecto.

## ⚡ Capa Plata (Evidencia 2)

**Rama de trabajo:** `silver-oscar`

**Alcance de esta documentación:** puntos 1 y 2 de la Capa Plata:
limpieza de EnerAndes y limpieza de las fuentes XM, IDEAM, NOAA y TRM.

**Entorno de ejecución:** Codespaces con Python 3.10+ y Pandas.

La Capa Plata recibe los datos crudos de `data/bronze/`, aplica reglas de
limpieza, deduplicación, tipado y validación de calidad, y genera archivos
optimizados en formato Parquet dentro de `data/silver/`. Los datos
inconsistentes o defectuosos se aíslan automáticamente en cuarentena.

### Resultados de la transformación

| Fuente | Archivo generado en `data/silver/` | Registros / filas | Observaciones / reglas aplicadas |
|---|---|---:|---|
| EnerAndes | `enerandes_ventas.parquet` | 4.007 | Unificación de las cuatro hojas, detección del encabezado real, fechas heterogéneas, conversión por unidad, normalización municipal y deduplicación. |
| EnerAndes | `enerandes_cuarentena.parquet` | 45 | Registros con fecha, energía, valor, clientes o municipio inválidos; se conserva el motivo de cuarentena. |
| XM | `xm_precio_bolsa.parquet` | 24.096 | Unpivot de 24 columnas horarias a formato vertical (`fecha`, `hora`, `precio_bolsa_kwh`). |
| XM | `xm_demanda.parquet` | 24.096 | Unpivot de 24 columnas horarias a formato vertical (`fecha`, `hora`, `demanda_kwh`). |
| XM | `xm_embalses.parquet` | 1.004 | Normalización de campos y eliminación de duplicados de volumen. |
| XM | `xm_generacion.parquet` | 5.935.449 | Generación horaria por fecha, hora y código de planta, procesada por bloques para controlar memoria. |
| XM | `xm_aportes.parquet` | 1.004 | Aportes diarios convertidos a número y deduplicados. |
| XM | `xm_listado_recursos.parquet` | 2.500 | Catálogo de plantas normalizado desde `ListadoRecursos`. |
| NOAA | `noaa_oni.parquet` | 920 | Mapeo de trimestres a meses (`YYYY-MM`), cálculo de anomalía y clasificación ENSO. |
| IDEAM | `ideam_precipitacion.parquet` | 2.374 | Limpieza de fechas, tipado numérico y eliminación de nulos. |
| IDEAM | `ideam_temperatura.parquet` | 1.477 | Conversión de comas decimales (`"22,5"` → `22.5`) y filtrado de lecturas válidas. |
| TRM | `trm_colombia.parquet` | 649 | Fecha como fecha, valor como número, eliminación de duplicados por día y orden cronológico. |

### Archivos modificados para los puntos 1 y 2

- [`src/silver/enerandes.py`](src/silver/enerandes.py) unifica las ventas de
  2023–2026, convierte MWh a kWh y envía a cuarentena las filas inválidas.
- [`src/silver/xm.py`](src/silver/xm.py) transforma las columnas `Hour01` a
  `Hour24` a un modelo tabular vertical para precio, demanda y generación;
  además limpia embalses, aportes y el catálogo `ListadoRecursos`.
- [`src/silver/noaa.py`](src/silver/noaa.py) traduce trimestres móviles
  (`DJF`, `JFM`, etc.) a meses (`YYYY-MM`) y clasifica las fases ENSO:
  El Niño (`ONI >= 0.5`), La Niña (`ONI <= -0.5`) o Neutral.
- [`src/silver/ideam.py`](src/silver/ideam.py) detecta columnas de fechas y
  valores numéricos, conserva estación y municipio e incluye la conversión de
  comas decimales.
- [`src/silver/trm.py`](src/silver/trm.py) limpia la fuente propia TRM y la
  guarda como una fila por fecha.

### Cambios de capa Plata — 2026-11-04

- EnerAndes ahora identifica el encabezado real aunque existan títulos y notas
  previas en las hojas 2025 y 2026.
- Se soportan fechas en español e inglés, `YYYY-MM`, `mar-24`, `03/2024` y
  `01/03/2026`, interpretando esta última como marzo de 2026.
- La conversión de energía se realiza según la unidad de cada fila: MWh se
  convierte a kWh y kWh se conserva sin alterar.
- Las filas no corregibles se conservan en cuarentena con la causa específica.
- XM quedó preparado para generar y limpiar generación, aportes y
  `ListadoRecursos`, además de precio, demanda y embalses.
- La generación XM se descargó por ventanas de 30 días y se transformó por
  bloques; se conservaron 633 códigos de planta y 5.935.449 filas horarias.
- IDEAM convierte explícitamente precipitación y las tres medidas de
  temperatura a números, conservando fecha, estación y municipio.
- NOAA consolida el ONI por mes central del trimestre móvil y calcula la fase
  ENSO con los umbrales solicitados.
- La TRM se incorporó a la capa plata como una fila numérica por fecha.

## Guía de trabajo para los puntos 1 y 2

Esta sección resume exactamente qué se hizo en los puntos 1 y 2. El flujo parte
de `data/bronze/` y escribe
los resultados en `data/silver/`; los archivos de datos no se suben al
repositorio porque están excluidos en `.gitignore`.

### Punto 1: EnerAndes

El módulo [src/silver/enerandes.py](src/silver/enerandes.py) procesa las
cuatro tablas bronce:

```text
data/bronze/enerandes_ventas_2023.parquet
data/bronze/enerandes_ventas_2024.parquet
data/bronze/enerandes_ventas_2025.parquet
data/bronze/enerandes_ventas_2026.parquet
```

No se asume que el encabezado está en la primera fila. El limpiador busca la
fila que contiene los nombres de negocio y elimina los títulos/notas previos.
Después aplica estas reglas:

- fechas estándar, meses abreviados y fechas con barra;
- interpretación de `01/03/2026` como marzo de 2026;
- conversión de MWh a kWh solo cuando la unidad de la fila es MWh;
- normalización de municipios y códigos DIVIPOLA;
- normalización de segmento y tipo de compra;
- conversión de energía, valor y clientes a números;
- deduplicación después de la normalización;
- envío a cuarentena de filas que no pueden corregirse.

La tabla limpia queda en `enerandes_ventas.parquet`. Las filas inválidas quedan
en `enerandes_cuarentena.parquet` y la columna `motivo_cuarentena` explica si
el problema fue fecha, energía, valor, clientes o municipio.

### Punto 2: fuentes restantes

#### XM

La configuración se encuentra en [src/config.py](src/config.py). Las métricas
son:

| Métrica | Frecuencia | Salida plata |
|---|---|---|
| `PrecBolsNaci` | Horaria | `xm_precio_bolsa.parquet` |
| `DemaReal` | Horaria | `xm_demanda.parquet` |
| `Gene` | Horaria por planta | `xm_generacion.parquet` |
| `AporEner` | Diaria | `xm_aportes.parquet` |
| `PorcVoluUtilDiar` | Diaria | `xm_embalses.parquet` |
| `ListadoRecursos` | Catálogo | `xm_listado_recursos.parquet` |

Las métricas horarias llegan con `Hour01`–`Hour24`. El módulo
[src/silver/xm.py](src/silver/xm.py) las convierte a una fila por fecha y
hora, convierte los valores a número y elimina duplicados. Para generación la
llave usa `code`, que identifica la planta; `Id` no sirve como llave porque
para todas las plantas llega como `Recurso`.

La generación es grande: tiene 5.935.449 filas, 633 códigos de planta y cubre
2024-01-01 a 2026-09-30. Por eso se descarga por ventanas de 30 días, se
guarda incrementalmente y se transforma por bloques para controlar memoria.
El catálogo contiene diccionarios anidados; estos se normalizan a columnas
`recurso_*` antes de guardarse.

#### IDEAM

El módulo [src/silver/ideam.py](src/silver/ideam.py) conserva el código,
nombre y municipio de cada estación. La fecha se convierte a tipo fecha y las
variables se convierten a números:

- `precipitacion_mm`;
- `temp_media`;
- `temp_min`;
- `temp_max`.

La extracción de IDEAM está limitada explícitamente al año 2025 completo:
`2025-01-01` a `2025-12-31`, dividido en ventanas de siete días. Se eliminaron
los límites artificiales que dejaban el año incompleto.

#### NOAA

El módulo [src/silver/noaa.py](src/silver/noaa.py) asigna cada trimestre móvil
al mes central: `DJF` a enero, `JFM` a febrero, hasta `NDJ` a diciembre. Luego
calcula la fase ENSO con los límites de la actividad:

```text
ONI >= 0.5  -> El Niño
ONI <= -0.5 -> La Niña
otro valor  -> Neutral
```

#### Fuente propia TRM

El módulo [src/silver/trm.py](src/silver/trm.py) convierte `vigenciadesde` a
fecha y `valor` a número, conserva la unidad, elimina duplicados por fecha y
genera `data/silver/trm_colombia.parquet`.

### Cómo ejecutar

El comando comprueba los insumos de Bronce, descarga los que falten sin
repetir los que ya existen, limpia las fuentes y construye las capas Plata y
Oro con dbt:

```bash
python -m src.transformar
```

Para volver a descargar todos los datos de Bronce, ignorando los archivos
existentes, se usa:

```bash
python -m src.pipeline --forzar
```

La descarga completa de XM puede tardar debido a las ventanas y al número de
plantas. No es necesario repetirla para reconstruir plata si los archivos
bronce ya están presentes.

Para comprobar que el código de limpieza sigue funcionando:

```bash
python -m pytest -q
```

La verificación realizada terminó con 19 pruebas aprobadas. Esta sección no
documenta los puntos posteriores de la actividad.
