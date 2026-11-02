# Reporte de Calidad de Datos - Capa Plata

## 1. Resumen Ejecutivo
La Capa Plata consolida, limpia y estandariza las fuentes de información de EnerAndes, XM, NOAA e IDEAM. Aplica reglas de validación con Pandera, aislamiento en cuarentena y exportación en formato optimizado Parquet (`data/silver/`).

---

## 2. Métricas y Reglas Aplicadas por Fuente

| Fuente | Archivo generado en `data/silver/` | Registros / Filas | Reglas de Calidad y Estandarización Aplicadas |
|---|---|---:|---|
| **EnerAndes** | `enerandes_ventas.parquet` | 2.019 | Unificación 2023–2026, conversión de MWh a kWh (`* 1000`), deduplicación y tipado de campos. |
| **EnerAndes** | `enerandes_cuarentena.parquet` | 25 | Aislamiento automático de registros con `energia_kwh <= 0`, valores nulos o DIVIPOLA erróneo. |
| **XM** | `xm_precio_bolsa.parquet` | 24.096 | Unpivot de 24 columnas horarias (`Hour01`–`Hour24`) a formato vertical (`fecha`, `hora`, `precio_bolsa_kwh`). |
| **XM** | `xm_demanda.parquet` | 24.096 | Unpivot de 24 columnas horarias a formato vertical (`fecha`, `hora`, `demanda_kwh`). |
| **XM** | `xm_embalses.parquet` | 1.004 | Normalización de campos y eliminación de registros duplicados de volumen útil. |
| **NOAA** | `noaa_oni.parquet` | 920 | Mapeo de trimestres móviles (`DJF`, `JFM`, etc.) a formato `YYYY-MM` y clasificación ENSO (El Niño: `ONI >= 0.5`, La Niña: `ONI <= -0.5`, Neutral). |
| **IDEAM** | `ideam_precipitacion.parquet` | 2.374 | Estandarización de fechas, conversión a tipo numérico y filtrado de registros nulos. |
| **IDEAM** | `ideam_temperatura.parquet` | 1.477 | Corrección de comas decimales (`"22,5"` → `22.5`) y filtrado de lecturas válidas. |

---

## 3. Validación de Esquemas y Contratos de Datos
- **Módulo:** `src/quality/esquemas.py`
- **Librería:** Pandera
- **Contratos:** Se definieron contratos estritos para validar tipos de datos, llaves primarias, rangos válidos (p. ej., `energia_kwh > 0`) y valores permitidos en columnas categóricas. Los registros que violan estos contratos son descartados o enviados a la tabla de cuarentena.

---

## 4. Pruebas Automatizadas (Pytest)
- **Ejecución:** `python -m pytest -v`
- **Resultado:** **18 de 18 pruebas aprobadas (100% PASSED)**
- **Cobertura clave:**
  1. Conversión de unidades MWh a kWh.
  2. Lógica de clasificación climática ENSO (El Niño / La Niña).
  3. Parseo y estandarización de fechas heterogéneas.
  4. Conversión de comas decimales a flotantes en mediciones IDEAM.
  5. Rechazo de tipos de compra inválidos vía esquemas de Pandera.