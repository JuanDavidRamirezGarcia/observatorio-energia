"""
Fuente 2 - IDEAM en datos.gov.co (plataforma Socrata, lenguaje de consulta SoQL).
  - El dataset tiene MILLONES de observaciones (una cada pocos minutos desde 2005)
  - Por eso FILTRAMOS ($where) y AGREGAMOS ($select + $group) EN EL SERVIDOR:
    viaja un resumen diario por estacion, no millones de filas
  - Ademas paginamos con $limit / $offset por si una ventana trae muchas filas
Documentacion SoQL: https://dev.socrata.com/docs/queries/
"""

# ---------------------------------------------------------------------------
# IMPORTS (traer codigo que ya existe)
# ---------------------------------------------------------------------------
import pandas as pd  # pandas: libreria de tablas. "as pd" le pone el nombre corto pd.

from src import (  # config.py de este proyecto: URL del IDEAM, departamento, fechas, ventana.
    config,
)
from src.utils import guardar_bronce, http_json, log, ventanas, ya_existe

# ---------------------------------------------------------------------------
# CONSTANTES: valores fijos de este extractor (en MAYUSCULAS por convencion)
# ---------------------------------------------------------------------------
NOMBRE_PRECIPITACION = (
    "ideam_precipitacion_diaria"  # nombre del archivo de precipitacion en bronce
)
CAMPOS = (
    "codigoestacion, nombreestacion, municipio, latitud, longitud"  # columnas que se piden
)
PAGINA = 50000  # filas maximas por pedido ($limit)

# [AGREGADO POR OSCAR]: Constantes para el dataset de Temperatura del aire (sbwg-7ju4)
NOMBRE_TEMPERATURA = "ideam_temperatura_diaria"
URL_TEMPERATURA = getattr(
    config,
    "IDEAM_TEMPERATURA_URL",
    "https://www.datos.gov.co/resource/sbwg-7ju4.json",
)


def consulta_soql_precipitacion(inicio, fin, offset: int) -> dict:
    """Arma los parametros SoQL: filtrar Antioquia y fechas, y sumar la lluvia por dia."""
    return {
        "$select": (
            f"{CAMPOS}, date_trunc_ymd(fechaobservacion) AS fecha, "
            "sum(valorobservado) AS precipitacion_mm, count(*) AS n_obs"
        ),
        "$where": (
            f"departamento = '{config.IDEAM_DEPARTAMENTO}' AND "
            f"fechaobservacion BETWEEN '{inicio}T00:00:00' AND '{fin}T23:59:59'"
        ),
        "$group": f"{CAMPOS}, fecha",
        "$order": "fecha, codigoestacion",
        "$limit": PAGINA,
        "$offset": offset,
    }


# [AGREGADO POR OSCAR]: Consulta SoQL para el dataset de Temperatura (sbwg-7ju4)
def consulta_soql_temperatura(inicio, fin, offset: int) -> dict:
    """Arma los parametros SoQL para calcular temp media, minima y maxima por dia y estacion."""
    return {
        "$select": (
            f"{CAMPOS}, date_trunc_ymd(fechaobservacion) AS fecha, "
            "avg(valorobservado) AS temp_media, "
            "min(valorobservado) AS temp_min, "
            "max(valorobservado) AS temp_max, count(*) AS n_obs"
        ),
        "$where": (
            f"departamento = '{config.IDEAM_DEPARTAMENTO}' AND "
            f"fechaobservacion BETWEEN '{inicio}T00:00:00' AND '{fin}T23:59:59'"
        ),
        "$group": f"{CAMPOS}, fecha",
        "$order": "fecha, codigoestacion",
        "$limit": PAGINA,
        "$offset": offset,
    }


# [AGREGADO POR OSCAR]: Funcion para extraer cualquier dataset SoQL descargando por semanas
def _extraer_dataset_ideam(
    nombre: str, url: str, funcion_consulta, forzar: bool = False
) -> None:
    """Descarga un dataset del IDEAM usando ventanas SoQL y guarda resultados en bronce y muestras."""
    if ya_existe(nombre, forzar):
        return

    filas = []
    # Utiliza config.IDEAM_FECHA_INICIO (actualizada a 2025-01-01 por Oscar)
    for i, (inicio, fin) in enumerate(
        ventanas(
            config.IDEAM_FECHA_INICIO, config.FECHA_FIN, config.IDEAM_DIAS_VENTANA
        )
    ):
        if i >= 10:  # [CONTADOR AGREGADO]: Detener el bucle al procesar 10 ventanas
            break

        offset = 0
        while True:
            lote = http_json(
                "GET", url, params=funcion_consulta(inicio, fin, offset)
            )
            filas.extend(lote)
            if len(lote) < PAGINA:
                break
            offset += PAGINA
        log(f"   semana {inicio} a {fin}: {len(lote)} filas")

    df = pd.DataFrame(filas)
    guardar_bronce(df, nombre, fuente="IDEAM", origen=url)


def extraer(forzar: bool = False) -> None:
    """Descarga la lluvia y temperatura diaria por estacion, semana por semana, y la guarda en bronce."""
    log("IDEAM - datos abiertos (SoQL)")

    # 1. Extraccion de Precipitaciones (Original de la clase)
    log("Extrayendo Precipitacion...")
    url_precipitacion = getattr(
        config,
        "IDEAM_PRECIPITACION_URL",
        getattr(
            config,
            "IDEAM_URL",
            "https://www.datos.gov.co/resource/s54a-sgyg.json",
        ),
    )
    _extraer_dataset_ideam(
        NOMBRE_PRECIPITACION,
        url_precipitacion,
        consulta_soql_precipitacion,
        forzar,
    )

    # [AGREGADO POR OSCAR]: 2. Extraccion del Dataset de Temperatura (sbwg-7ju4)
    log("Extrayendo Temperatura (dataset sbwg-7ju4)...")
    _extraer_dataset_ideam(
        NOMBRE_TEMPERATURA, URL_TEMPERATURA, consulta_soql_temperatura, forzar
    )


# ---------------------------------------------------------------------------
# Este bloque solo se ejecuta cuando se corre ESTE archivo directamente:
#     python -m src.extract.ideam
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    extraer(forzar="--forzar" in sys.argv)