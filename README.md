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

