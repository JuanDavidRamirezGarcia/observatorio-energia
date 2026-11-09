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
| XM – API Sinergox | API REST, respuestas JSON | Precio de bolsa, demanda real y porcentaje de volumen útil diario de embalses | `xm_precio_bolsa.parquet`, `xm_demanda.parquet`, `xm_embalses.parquet` |
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

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
# copiar ventas_enerandes_2023_2026.xlsx en data/insumos/
python -m src.pipeline          # descarga las 4 fuentes a data/bronze/ (unos 3 minutos)
python -m src.consultar         # consultas SQL de BI con DuckDB
python -m pytest                # muestra el resultado de cada prueba (configurado en pytest.ini)
```

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
| Medellín | 173105.78 |
| Bello | 55326.51 |
| Itagüí | 37775.61 |
| Envigado | 26613.45 |
| Rionegro | 26011.43 |
| Sabaneta | 19165.63 |
| Apartadó | 18347.56 |
| Turbo | 13721.23 |
| La Estrella | 11329.72 |
| Caldas | 11053.32 |

### 2) Promedio de precio de bolsa por hora y fase ENSO

| Hora | Fase ENSO | Precio promedio (COP/kWh) |
|---:|---|---:|
| 1 | El Niño | 619.39 |
| 2 | El Niño | 615.51 |
| 3 | El Niño | 606.36 |
| 4 | El Niño | 602.41 |
| 5 | El Niño | 613.39 |
| 6 | El Niño | 630.27 |
| 7 | El Niño | 616.46 |
| 8 | El Niño | 593.46 |
| 9 | El Niño | 581.85 |
| 10 | El Niño | 577.50 |

### 3) Comparativo horario de generación vs demanda

| Hora | Generación (MWh) | Demanda (MWh) | Diferencia (MWh) |
|---:|---:|---:|---:|
| 1 | 8.71 | 8.71 | 0.00 |
| 2 | 8.42 | 8.42 | 0.00 |
| 3 | 8.20 | 8.20 | 0.00 |
| 4 | 8.08 | 8.08 | 0.00 |
| 5 | 8.17 | 8.17 | 0.00 |
| 6 | 8.40 | 8.40 | 0.00 |
| 7 | 8.50 | 8.50 | 0.00 |
| 8 | 8.91 | 8.91 | 0.00 |
| 9 | 9.34 | 9.34 | 0.00 |
| 10 | 9.63 | 9.63 | 0.00 |

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

**Rama de trabajo:** `feature/plata-oro`

**Alcance de la entrega:** puntos 1 al 4 (Capa Plata, Pandera, Pytest,
reporte de calidad y orquestación de limpieza).

**Entorno de ejecución:** Codespaces con Python 3.10+, Pandas, Pandera y
Pytest.

La Capa Plata recibe los datos crudos de `data/bronze/`, aplica reglas de
limpieza, deduplicación, tipado y validación de calidad, y genera archivos
optimizados en formato Parquet dentro de `data/silver/`. Los datos
inconsistentes o defectuosos se aíslan automáticamente en cuarentena.

### Resultados de la transformación

| Fuente | Archivo generado en `data/silver/` | Registros / filas | Observaciones / reglas aplicadas |
|---|---|---:|---|
| EnerAndes | `enerandes_ventas.parquet` | 2.019 | Conversión de MWh a kWh (`* 1000`), eliminación de duplicados y normalización de campos. |
| EnerAndes | `enerandes_cuarentena.parquet` | 25 | Registros con kWh menor o igual a cero, valores nulos o DIVIPOLA erróneo. |
| XM | `xm_precio_bolsa.parquet` | 24.096 | Unpivot de 24 columnas horarias a formato vertical (`fecha`, `hora`, `precio_bolsa_kwh`). |
| XM | `xm_demanda.parquet` | 24.096 | Unpivot de 24 columnas horarias a formato vertical (`fecha`, `hora`, `demanda_kwh`). |
| XM | `xm_embalses.parquet` | 1.004 | Normalización de campos y eliminación de duplicados de volumen. |
| NOAA | `noaa_oni.parquet` | 920 | Mapeo de trimestres a meses (`YYYY-MM`), cálculo de anomalía y clasificación ENSO. |
| IDEAM | `ideam_precipitacion.parquet` | 2.374 | Limpieza de fechas, tipado numérico y eliminación de nulos. |
| IDEAM | `ideam_temperatura.parquet` | 1.477 | Conversión de comas decimales (`"22,5"` → `22.5`) y filtrado de lecturas válidas. |

### Módulos de limpieza y transformación

- [`src/silver/enerandes.py`](src/silver/enerandes.py) unifica las ventas de
  2023–2026, convierte MWh a kWh y envía a cuarentena las filas inválidas.
- [`src/silver/xm.py`](src/silver/xm.py) transforma las columnas `Hour01` a
  `Hour24` a un modelo tabular vertical para precios y demanda, y procesa los
  embalses.
- [`src/silver/noaa.py`](src/silver/noaa.py) traduce trimestres móviles
  (`DJF`, `JFM`, etc.) a meses (`YYYY-MM`) y clasifica las fases ENSO:
  El Niño (`ONI >= 0.5`), La Niña (`ONI <= -0.5`) o Neutral.
- [`src/silver/ideam.py`](src/silver/ideam.py) detecta columnas de fechas y
  valores numéricos, incluyendo la conversión de comas decimales.

### Esquemas, calidad y orquestación

- [`src/quality/esquemas.py`](src/quality/esquemas.py) define los contratos de
  datos con Pandera y valida llaves, rangos, nulos y tipos antes de guardar
  los Parquet.
- [`src/transformar.py`](src/transformar.py) ejecuta secuencialmente la
  limpieza de EnerAndes, NOAA, XM e IDEAM:

  ```bash
  python -m src.transformar
  ```

- Las pruebas automatizadas se ejecutan con:

  ```bash
  python -m pytest -v
  ```

  La suite de referencia de esta entrega contiene 13 pruebas aprobadas.

### Insumos para la Capa Oro

Los archivos Parquet disponibles para dbt y DuckDB son:

- `data/silver/enerandes_ventas.parquet`
- `data/silver/xm_precio_bolsa.parquet`
- `data/silver/xm_demanda.parquet`
- `data/silver/xm_embalses.parquet`
- `data/silver/noaa_oni.parquet`
- `data/silver/ideam_precipitacion.parquet`
- `data/silver/ideam_temperatura.parquet`

Para integrarse con esta entrega, usar la rama `feature/plata-oro` o aprobar
el Pull Request correspondiente hacia `main`.
