"""
Capa PLATA: Limpia las variables de precipitación y temperatura del IDEAM.
"""
import pandas as pd
from src import config
from src.quality.esquemas import (
    ESQUEMA_IDEAM_PRECIPITACION,
    ESQUEMA_IDEAM_TEMPERATURA,
)
from src.utils import log

LINAJE = ["_fuente", "_origen", "_extraido_en"]

def limpiar_ideam_variable(nombre_archivo: str, nombre_col_valor: str) -> pd.DataFrame:
    ruta = config.DIR_BRONZE / f"ideam_{nombre_archivo}_diaria.parquet"
    if not ruta.exists():
        ruta = config.DIR_BRONZE / f"ideam_{nombre_archivo}.parquet"
        if not ruta.exists():
            log(f" No se encontró archivo en bronce para IDEAM {nombre_archivo}")
            return pd.DataFrame()
        
    df = pd.read_parquet(ruta).drop(columns=LINAJE, errors="ignore")
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    # Identificar columna de fecha
    cols_fecha = [c for c in df.columns if any(x in c for x in ["fecha", "time", "date"])]
    col_fecha = cols_fecha[0] if cols_fecha else df.columns[0]
    
    df["fecha"] = pd.to_datetime(df[col_fecha], errors="coerce")
    if nombre_archivo == "precipitacion":
        columnas_valor = ["precipitacion_mm"]
    else:
        columnas_valor = ["temp_media", "temp_min", "temp_max"]
    for columna in columnas_valor:
        if columna in df.columns:
            serie_val = df[columna].astype(str).str.replace(",", ".", regex=False)
            df[columna] = pd.to_numeric(serie_val, errors="coerce").astype(float)
    for columna in ["latitud", "longitud", "n_obs"]:
        if columna in df.columns:
            serie = df[columna].astype(str).str.replace(",", ".", regex=False)
            df[columna] = pd.to_numeric(serie, errors="coerce")

    if nombre_archivo == "temperatura" and "temp_media" in df.columns:
        df[nombre_col_valor] = df["temp_media"]

    df_limpio = (
        df.dropna(subset=["fecha", nombre_col_valor])
        .drop_duplicates(subset=["codigoestacion", "fecha"])
        .reset_index(drop=True)
    )
    return df_limpio

def main():
    log("Iniciando limpieza de fuentes IDEAM...")
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    
    df_prep = limpiar_ideam_variable("precipitacion", "precipitacion_mm")
    if not df_prep.empty:
        ESQUEMA_IDEAM_PRECIPITACION.validate(df_prep, lazy=True)
        df_prep.to_parquet(config.DIR_SILVER / "ideam_precipitacion.parquet", index=False)
        log(f"Plata IDEAM Precipitación: {len(df_prep)} registros guardados.")

    df_temp = limpiar_ideam_variable("temperatura", "temperatura_celsius")
    if not df_temp.empty:
        ESQUEMA_IDEAM_TEMPERATURA.validate(df_temp, lazy=True)
        df_temp.to_parquet(config.DIR_SILVER / "ideam_temperatura.parquet", index=False)
        log(f"Plata IDEAM Temperatura: {len(df_temp)} registros guardados.")

if __name__ == "__main__":
    main()