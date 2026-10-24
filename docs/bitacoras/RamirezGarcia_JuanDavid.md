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