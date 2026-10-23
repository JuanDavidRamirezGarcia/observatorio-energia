"""
Fuente 1 - API REST de XM (operador del mercado eléctrico colombiano).
  - Método POST con un cuerpo JSON
  - Máximo 30 días por consulta -> pedimos por VENTANAS (para hourly/daily)
  - Endpoint 'lists' para catálogos/listados (sin rango de fechas)
  - No requiere usuario ni clave
Documentación: https://github.com/EquipoAnaliticaXM/API_XM
"""

import pandas as pd
from src import config
from src.utils import guardar_bronce, http_json, log, ventanas, ya_existe


def aplanar(respuesta: dict, periodo: str) -> list:
    """Convierte el JSON anidado de XM en filas planas, SIN cambiar los valores."""
    filas = []
    for item in respuesta.get("Items", []):
        if periodo == "hourly":
            for entidad in item.get("HourlyEntities", []):
                filas.append({"Date": item["Date"], "Id": entidad["Id"], **entidad["Values"]})
        elif periodo == "lists":
            # Estructura especial para el endpoint de listas/catálogos
            for entidad in item.get("ListEntities", []):
                filas.append(entidad)
        else:  # daily
            for entidad in item.get("DailyEntities", []):
                filas.append({"Date": item["Date"], "Id": entidad["Id"], "Value": entidad["Value"]})
    return filas


def extraer_metrica(metrica: str, entidad: str, periodo: str, nombre: str, forzar: bool) -> None:
    """Descarga una métrica de XM y la guarda en bronce.
    
    Soporta consultas históricas por ventanas (hourly/daily) y consultas
    de catálogo sin fechas (lists).
    """
    if ya_existe(nombre, forzar):
        return

    url = config.XM_URL.format(periodo=periodo)

    # -----------------------------------------------------------------------
    # Caso 1: Endpoint 'lists' (Catálogos como ListadoRecursos)
    # No requiere rango de fechas ni iteración por ventanas.
    # -----------------------------------------------------------------------
    if periodo == "lists":
        cuerpo = {"MetricId": metrica}
        respuesta = http_json("POST", url, json=cuerpo)
        filas = aplanar(respuesta, periodo)
        log(f"   {metrica}: {len(filas)} recursos en catálogo registrados")
        guardar_bronce(pd.DataFrame(filas), nombre, fuente="XM", origen=f"{url} MetricId={metrica}")
        return

    # -----------------------------------------------------------------------
    # Caso 2: Métricas temporales (hourly / daily)
    # Requieren iterar en ventanas de máximo 30 días.
    # -----------------------------------------------------------------------
    filas = []
    for inicio, fin in ventanas(config.FECHA_INICIO, config.FECHA_FIN, config.XM_MAX_DIAS):
        cuerpo = {
            "MetricId": metrica,
            "Entity": entidad,
            "StartDate": str(inicio),
            "EndDate": str(fin),
            "Filter": []
        }
        respuesta = http_json("POST", url, json=cuerpo)
        nuevas = aplanar(respuesta, periodo)
        filas.extend(nuevas)
        log(f"   {metrica} {inicio} a {fin}: {len(nuevas)} filas")

    guardar_bronce(pd.DataFrame(filas), nombre, fuente="XM", origen=f"{url} MetricId={metrica}")


def extraer(forzar: bool = False) -> None:
    """Descarga todas las métricas de XM definidas en config.XM_METRICAS."""
    log("XM - API REST del mercado eléctrico")
    for metrica, entidad, periodo, nombre in config.XM_METRICAS:
        extraer_metrica(metrica, entidad, periodo, nombre, forzar)


if __name__ == "__main__":
    import sys
    extraer(forzar="--forzar" in sys.argv)
