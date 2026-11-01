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

