"""Limpieza de la fuente propia TRM para la capa plata."""

import pandas as pd

from src import config
from src.utils import log


def limpiar_trm(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.drop(columns=["_fuente", "_origen", "_extraido_en"], errors="ignore").copy()
    df["fecha"] = pd.to_datetime(df["vigenciadesde"], errors="coerce")
    df["trm_cop"] = pd.to_numeric(
        df["valor"].astype(str).str.replace(",", ".", regex=False),
        errors="coerce",
    )
    columnas = ["fecha", "trm_cop", "unidad"]
    return (
        df.dropna(subset=["fecha", "trm_cop"])
        .loc[:, [c for c in columnas if c in df.columns]]
        .drop_duplicates(subset=["fecha"])
        .sort_values("fecha")
        .reset_index(drop=True)
    )


def main() -> None:
    ruta = config.DIR_BRONZE / "trm_colombia.parquet"
    if not ruta.exists():
        log(f"No se encontró archivo TRM en bronce: {ruta}")
        return
    limpio = limpiar_trm(pd.read_parquet(ruta))
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    limpio.to_parquet(config.DIR_SILVER / "trm_colombia.parquet", index=False)
    log(f"Plata TRM: {len(limpio)} registros.")


if __name__ == "__main__":
    main()
