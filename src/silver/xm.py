"""
Capa PLATA: Limpia las fuentes de XM (Precio de bolsa, Demanda y Embalses).
"""
import pandas as pd
from src import config
from src.quality.esquemas import ESQUEMA_XM_HORARIO
from src.utils import log

LINAJE = ["_fuente", "_origen", "_extraido_en"]

def unpivot_24_horas(df_raw: pd.DataFrame, nombre_valor: str) -> pd.DataFrame:
    df = df_raw.drop(columns=LINAJE, errors="ignore").copy()
    cols_horas = [c for c in df.columns if str(c).startswith("Hour")]
    cols_id = [c for c in df.columns if c not in cols_horas]
    
    df_melt = df.melt(id_vars=cols_id, value_vars=cols_horas, var_name="hora_str", value_name=nombre_valor)
    df_melt["hora"] = df_melt["hora_str"].str.extract(r"(\d+)").astype(int)
    
    col_fecha = next((c for c in cols_id if "fecha" in str(c).lower()), cols_id[0])
    df_melt["fecha"] = pd.to_datetime(df_melt[col_fecha], errors="coerce")
    df_melt[nombre_valor] = pd.to_numeric(df_melt[nombre_valor], errors="coerce")
    
    df_limpio = df_melt.dropna(subset=["fecha", nombre_valor]).copy()
    return df_limpio.sort_values(by=["fecha", "hora"]).reset_index(drop=True)

def main():
    log("Iniciando limpieza de fuentes XM...")
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    
    ruta_precio = config.DIR_BRONZE / "xm_precio_bolsa.parquet"
    if ruta_precio.exists():
        df_precio = pd.read_parquet(ruta_precio)
        df_p_limpio = unpivot_24_horas(df_precio, "precio_bolsa_kwh")
        df_p_limpio.to_parquet(config.DIR_SILVER / "xm_precio_bolsa.parquet", index=False)
        log(f"Plata XM Precio Bolsa: {len(df_p_limpio)} filas horarias.")

    ruta_demanda = config.DIR_BRONZE / "xm_demanda.parquet"
    if ruta_demanda.exists():
        df_demanda = pd.read_parquet(ruta_demanda)
        df_d_limpia = unpivot_24_horas(df_demanda, "demanda_kwh")
        df_d_limpia.to_parquet(config.DIR_SILVER / "xm_demanda.parquet", index=False)
        log(f"Plata XM Demanda: {len(df_d_limpia)} filas horarias.")

    ruta_embalses = config.DIR_BRONZE / "xm_embalses.parquet"
    if ruta_embalses.exists():
        df_emb = pd.read_parquet(ruta_embalses).drop(columns=LINAJE, errors="ignore").drop_duplicates()
        df_emb.to_parquet(config.DIR_SILVER / "xm_embalses.parquet", index=False)
        log(f"Plata XM Embalses: {len(df_emb)} registros.")

if __name__ == "__main__":
    main()