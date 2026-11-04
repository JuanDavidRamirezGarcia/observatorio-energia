"""Limpia las fuentes de XM y normaliza sus métricas a la capa plata."""
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
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
    
    llave_recurso = "code" if "code" in df_melt.columns else "Id"
    df_limpio = (
        df_melt.dropna(subset=["fecha", nombre_valor])
        .drop_duplicates(subset=["fecha", "hora", llave_recurso])
        .copy()
    )
    return df_limpio.sort_values(by=["fecha", "hora"]).reset_index(drop=True)


def limpiar_diario(df_raw: pd.DataFrame, nombre_valor: str) -> pd.DataFrame:
    df = df_raw.drop(columns=LINAJE, errors="ignore").copy()
    fecha = next((c for c in df.columns if str(c).lower() in {"date", "fecha"}), df.columns[0])
    df["fecha"] = pd.to_datetime(df[fecha], errors="coerce")
    df[nombre_valor] = pd.to_numeric(df.get("Value"), errors="coerce")
    return (
        df.dropna(subset=["fecha", nombre_valor])
        .drop_duplicates(subset=["fecha", "Id"])
        .sort_values(["fecha", "Id"])
        .reset_index(drop=True)
    )


def limpiar_catalogo(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.drop(columns=LINAJE, errors="ignore").copy()
    if "Values" in df.columns:
        valores = pd.json_normalize(df["Values"]).add_prefix("recurso_")
        df = pd.concat([df.drop(columns=["Values"]), valores], axis=1)
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df.dropna(how="all").drop_duplicates().reset_index(drop=True)


def limpiar_horario_por_bloques(
    ruta_bronce, nombre_valor: str, ruta_salida, tamano_bloque: int = 20_000
) -> int:
    df_raw = pd.read_parquet(ruta_bronce)
    escritor = None
    filas_totales = 0
    try:
        for inicio in range(0, len(df_raw), tamano_bloque):
            bloque = unpivot_24_horas(
                df_raw.iloc[inicio:inicio + tamano_bloque], nombre_valor
            )
            if bloque.empty:
                continue
            tabla = pa.Table.from_pandas(bloque, preserve_index=False)
            if escritor is None:
                escritor = pq.ParquetWriter(ruta_salida, tabla.schema)
            escritor.write_table(tabla)
            filas_totales += len(bloque)
    finally:
        if escritor is not None:
            escritor.close()
    return filas_totales


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

    ruta_generacion = config.DIR_BRONZE / "xm_generacion.parquet"
    if ruta_generacion.exists():
        filas = limpiar_horario_por_bloques(
            ruta_generacion,
            "generacion_mwh",
            config.DIR_SILVER / "xm_generacion.parquet",
        )
        log(f"Plata XM Generación: {filas} filas horarias.")

    ruta_embalses = config.DIR_BRONZE / "xm_embalses.parquet"
    if ruta_embalses.exists():
        df_emb = limpiar_diario(pd.read_parquet(ruta_embalses), "embalses_pct")
        df_emb.to_parquet(config.DIR_SILVER / "xm_embalses.parquet", index=False)
        log(f"Plata XM Embalses: {len(df_emb)} registros.")

    ruta_aportes = config.DIR_BRONZE / "xm_aportes.parquet"
    if ruta_aportes.exists():
        df_aportes = limpiar_diario(pd.read_parquet(ruta_aportes), "aportes_mwh")
        df_aportes.to_parquet(config.DIR_SILVER / "xm_aportes.parquet", index=False)
        log(f"Plata XM Aportes: {len(df_aportes)} registros.")

    ruta_catalogo = config.DIR_BRONZE / "xm_listado_recursos.parquet"
    if ruta_catalogo.exists():
        df_catalogo = limpiar_catalogo(pd.read_parquet(ruta_catalogo))
        df_catalogo.to_parquet(
            config.DIR_SILVER / "xm_listado_recursos.parquet", index=False
        )
        log(f"Plata XM ListadoRecursos: {len(df_catalogo)} registros.")

if __name__ == "__main__":
    main()