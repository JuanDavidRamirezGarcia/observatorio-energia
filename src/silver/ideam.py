"""
Capa PLATA: Limpia las variables de precipitación y temperatura del IDEAM.
"""
import pandas as pd
from src import config
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
    
    # Identificar columna de valor numérico
    cols_valor = [c for c in df.columns if any(x in c for x in ["valor", "val", "precipitacion", "temperatura", "medida", "dato"])]
    if cols_valor:
        col_valor = cols_valor[0]
    else:
        candidatas = [c for c in df.columns if c != col_fecha]
        col_valor = candidatas[0] if candidatas else df.columns[0]
    
    df["fecha"] = pd.to_datetime(df[col_fecha], errors="coerce")
    
    # Reemplazar comas decimales por puntos antes de convertir a número
    serie_val = df[col_valor].astype(str).str.replace(",", ".", regex=False)
    df[nombre_col_valor] = pd.to_numeric(serie_val, errors="coerce")
    
    df_limpio = df.dropna(subset=["fecha", nombre_col_valor]).drop_duplicates().reset_index(drop=True)
    return df_limpio

def main():
    log("Iniciando limpieza de fuentes IDEAM...")
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    
    df_prep = limpiar_ideam_variable("precipitacion", "precipitacion_mm")
    if not df_prep.empty:
        df_prep.to_parquet(config.DIR_SILVER / "ideam_precipitacion.parquet", index=False)
        log(f"Plata IDEAM Precipitación: {len(df_prep)} registros guardados.")

    df_temp = limpiar_ideam_variable("temperatura", "temperatura_celsius")
    if not df_temp.empty:
        df_temp.to_parquet(config.DIR_SILVER / "ideam_temperatura.parquet", index=False)
        log(f"Plata IDEAM Temperatura: {len(df_temp)} registros guardados.")

if __name__ == "__main__":
    main()