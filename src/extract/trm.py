"""
Fuente Adicional - TRM (Tasa Representativa del Mercado)
  - Origen: Banco de la República vía Datos Abiertos Colombia (API Socrata)
  - Método: GET
"""

import pandas as pd
from src import config
from src.utils import guardar_bronce, http_json, log, ya_existe


def extraer(forzar: bool = False) -> None:
    """Descarga la TRM diaria desde la API de Datos Abiertos y la guarda en bronce."""
    nombre = "trm_colombia"
    if ya_existe(nombre, forzar):
        return

    log("TRM - Tasa Representativa del Mercado (Datos Abiertos Colombia)")

    # Parámetros de consulta usando las constantes de config.py
    params = {
        "$limit": 5000,
        "$where": f"vigenciadesde >= '{config.FECHA_INICIO}' AND vigenciadesde <= '{config.FECHA_FIN}'",
        "$order": "vigenciadesde ASC"
    }

    respuesta = http_json("GET", config.TRM_URL, params=params)

    if respuesta:
        df = pd.DataFrame(respuesta)
        log(f"   TRM: {len(df)} registros descargados ({config.FECHA_INICIO} a {config.FECHA_FIN})")
        guardar_bronce(df, nombre, fuente="Datos Abiertos - Banco de la República", origen=config.TRM_URL)
    else:
        log("   Advertencia: No se obtuvieron registros de TRM.")


if __name__ == "__main__":
    import sys
    extraer(forzar="--forzar" in sys.argv)