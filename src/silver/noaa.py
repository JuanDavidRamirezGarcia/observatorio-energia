"""
Capa PLATA: Limpia el índice ONI de la NOAA y calcula la fase ENSO.
"""
import pandas as pd
from src import config
from src.quality.esquemas import ESQUEMA_NOAA
from src.utils import log

TRIMESTRE_A_MES = {
    "DJF": "01", "JFM": "02", "FMA": "03", "MAM": "04",
    "AMJ": "05", "MJJ": "06", "JJA": "07", "JAS": "08",
    "ASO": "09", "SON": "10", "OND": "11", "NDJ": "12"
}

def calcular_fase_enso(oni: float) -> str:
    if oni >= 0.5: return "El Niño"
    if oni <= -0.5: return "La Niña"
    return "Neutral"

def main():
    log("Iniciando limpieza de datos NOAA (ONI)...")
    ruta = config.DIR_BRONZE / "noaa_oni.parquet"
    if not ruta.exists():
        log(f" No se encontró el archivo de bronce: {ruta}")
        return

    df = pd.read_parquet(ruta)
    df["mes_num"] = df["SEAS"].map(TRIMESTRE_A_MES)
    df["periodo"] = df["YR"].astype(str) + "-" + df["mes_num"]
    df["oni"] = pd.to_numeric(df["ANOM"], errors="coerce")
    df["fase_enso"] = df["oni"].apply(calcular_fase_enso)

    df_limpio = df[["periodo", "oni", "fase_enso"]].dropna().drop_duplicates()
    ESQUEMA_NOAA.validate(df_limpio, lazy=True)

    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    df_limpio.to_parquet(config.DIR_SILVER / "noaa_oni.parquet", index=False)
    log(f"Plata NOAA: {len(df_limpio)} registros de ONI guardados.")

if __name__ == "__main__":
    main()