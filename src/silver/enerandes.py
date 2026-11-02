"""
Capa PLATA: Limpia las 4 hojas del Excel de EnerAndes (2023 a 2026) y las unifica.
"""
from datetime import datetime
import unicodedata
import pandas as pd
from src import config
from src.quality.esquemas import ESQUEMA_VENTAS
from src.utils import log

LINAJE = ["_fuente", "_origen", "_extraido_en"]

MESES_ESP = {
    "ene": "01", "feb": "02", "mar": "03", "abr": "04",
    "may": "05", "jun": "06", "jul": "07", "ago": "08",
    "sep": "09", "oct": "10", "nov": "11", "dic": "12"
}

MUNICIPIOS = {
    "medellin": ("05001", "Medellín"),
    "santa fe de antioquia": ("05042", "Santa Fe de Antioquia"),
    "apartado": ("05045", "Apartadó"),
    "bello": ("05088", "Bello"),
    "caldas": ("05129", "Caldas"),
    "caucasia": ("05154", "Caucasia"),
    "copacabana": ("05212", "Copacabana"),
    "envigado": ("05266", "Envigado"),
    "girardota": ("05308", "Girardota"),
    "itagui": ("05360", "Itagüí"),
    "la estrella": ("05380", "La Estrella"),
    "marinilla": ("05440", "Marinilla"),
    "rionegro": ("05615", "Rionegro"),
    "sabaneta": ("05631", "Sabaneta"),
    "turbo": ("05837", "Turbo"),
}

ALIAS_MUNICIPIO = {
    "rio negro": "rionegro", "rionegro (ant)": "rionegro",
    "medellin d.e.": "medellin", "sta fe de antioquia": "santa fe de antioquia",
    "santafe de antioquia": "santa fe de antioquia"
}

def sin_tildes(texto: str) -> str:
    if pd.isna(texto): return ""
    letras = unicodedata.normalize("NFD", str(texto).strip().lower())
    return "".join(c for c in letras if unicodedata.category(c) != "Mn")

def estandarizar_fecha(val) -> str | None:
    if pd.isna(val): return None
    if isinstance(val, (pd.Timestamp, datetime)):
        if 2020 <= val.year <= 2030:
            return val.strftime("%Y-%m")
        return None

    s = str(val).strip()
    if "TOTAL" in s.upper(): return "TOTAL"
    
    # Manejo de formatos tipo mar-24 o dic-2023
    if "-" in s:
        partes = s.lower().split("-")
        if len(partes) == 2:
            m_str, y_str = partes[0].strip(), partes[1].strip()
            if m_str in MESES_ESP:
                mes = MESES_ESP[m_str]
                anio = f"20{y_str}" if len(y_str) == 2 else y_str
                if 2020 <= int(anio) <= 2030:
                    return f"{anio}-{mes}"

    # Manejo de formatos con slash (01/03/2026 o 03/2024)
    if "/" in s:
        partes = s.split("/")
        if len(partes) == 3 and len(partes[2]) == 4:
            dt = pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
            if pd.notna(dt) and 2020 <= dt.year <= 2030:
                return dt.strftime("%Y-%m")
        elif len(partes) == 2:
            dt = pd.to_datetime(s, format="%m/%Y", errors="coerce")
            if pd.notna(dt) and 2020 <= dt.year <= 2030:
                return dt.strftime("%Y-%m")

    # Formatos estándar YYYY-MM
    dt = pd.to_datetime(s, errors="coerce")
    if pd.notna(dt) and 2020 <= dt.year <= 2030:
        return dt.strftime("%Y-%m")
        
    return None

def clave_municipio(texto) -> str | None:
    if pd.isna(texto): return None
    clave = sin_tildes(texto)
    return ALIAS_MUNICIPIO.get(clave, clave)

def normalizar_segmento(val) -> str:
    if pd.isna(val): return "No informado"
    s = sin_tildes(str(val))
    if "res" in s: return "Residencial"
    if "com" in s: return "Comercial"
    if "ind" in s: return "Industrial"
    return "No informado"

def normalizar_tipo_compra(val) -> str:
    if pd.isna(val): return "Contrato"
    s = sin_tildes(str(val))
    if "bol" in s: return "Bolsa"
    if "con" in s: return "Contrato"
    return "Contrato"

def normalizar_encabezados(df: pd.DataFrame) -> pd.DataFrame:
    cols_str = [sin_tildes(str(c)) for c in df.columns]
    
    if not any(k in cols_str for k in ["fecha", "periodo", "municipio", "segmento", "modalidad", "energia"]):
        df.columns = [str(x) for x in df.iloc[0].tolist()]
        df = df.iloc[1:].copy()

    nuevos_nombres = {}
    for col in df.columns:
        c_clean = sin_tildes(str(col)).replace(" ", "_")
        if any(x in c_clean for x in ["fecha", "periodo"]):
            nuevos_nombres[col] = "periodo"
        elif "municipio" in c_clean:
            nuevos_nombres[col] = "municipio"
        elif "segmento" in c_clean:
            nuevos_nombres[col] = "segmento"
        elif any(x in c_clean for x in ["modalidad", "compra", "tipo"]):
            nuevos_nombres[col] = "tipo_compra"
        elif "energia" in c_clean:
            nuevos_nombres[col] = "energia_kwh"
        elif "valor" in c_clean:
            nuevos_nombres[col] = "valor_cop"
        elif "cliente" in c_clean:
            nuevos_nombres[col] = "clientes"

    df = df.rename(columns=nuevos_nombres)
    df = df.loc[:, ~df.columns.duplicated()].copy()

    for c in ["periodo", "municipio", "segmento", "tipo_compra", "energia_kwh", "valor_cop", "clientes"]:
        if c not in df.columns:
            df[c] = None

    return df

def limpiar_hoja(df_raw: pd.DataFrame, anio: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df_raw.drop(columns=LINAJE, errors="ignore").copy()
    
    df = normalizar_encabezados(df)
    df["periodo"] = df["periodo"].apply(estandarizar_fecha)
    df = df[df["periodo"] != "TOTAL"].dropna(subset=["periodo"])
    
    df["energia_kwh"] = pd.to_numeric(df["energia_kwh"], errors="coerce")
    if anio == 2024:
        df["energia_kwh"] = df["energia_kwh"] * 1000.0

    df["valor_cop"] = pd.to_numeric(df["valor_cop"], errors="coerce")
    df["clientes"] = pd.to_numeric(df["clientes"], errors="coerce").fillna(0).astype(int)

    df["clave_mun"] = df["municipio"].apply(clave_municipio)
    df["divipola"] = df["clave_mun"].apply(lambda c: MUNICIPIOS.get(c, (None, None))[0])
    df["municipio"] = df["clave_mun"].apply(lambda c: MUNICIPIOS.get(c, (None, None))[1])
    
    df["segmento"] = df["segmento"].apply(normalizar_segmento)
    df["tipo_compra"] = df["tipo_compra"].apply(normalizar_tipo_compra)

    malas = df["energia_kwh"].isna() | (df["energia_kwh"] < 0) | df["divipola"].isna()
    cuarentena = df[malas].copy()
    limpias = df[~malas].copy()

    return limpias, cuarentena

def main():
    log("Iniciando limpieza unificada EnerAndes (2023-2026)...")
    limpias_list, cuarentena_list = [], []

    for anio in range(2023, 2027):
        ruta = config.DIR_BRONZE / f"enerandes_ventas_{anio}.parquet"
        if ruta.exists():
            df_bronce = pd.read_parquet(ruta)
            l, c = limpiar_hoja(df_bronce, anio)
            limpias_list.append(l)
            cuarentena_list.append(c)

    if not limpias_list:
        log("No se encontraron archivos en la capa bronce.")
        return

    df_final = pd.concat(limpias_list, ignore_index=True)
    df_cuarentena = pd.concat(cuarentena_list, ignore_index=True) if cuarentena_list else pd.DataFrame()

    orden = ["periodo", "divipola", "municipio", "segmento", "tipo_compra", "energia_kwh", "valor_cop", "clientes"]
    df_final = df_final[orden]

    df_final = df_final.groupby(
        ["periodo", "divipola", "municipio", "segmento", "tipo_compra"],
        as_index=False
    ).agg({
        "energia_kwh": "sum",
        "valor_cop": "sum",
        "clientes": "max"
    }).reset_index(drop=True)

    ESQUEMA_VENTAS.validate(df_final, lazy=True)
    
    config.DIR_SILVER.mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(config.DIR_SILVER / "enerandes_ventas.parquet", index=False)
    if not df_cuarentena.empty:
        df_cuarentena.to_parquet(config.DIR_SILVER / "enerandes_cuarentena.parquet", index=False)
    log(f"Plata EnerAndes: {len(df_final)} filas limpias y {len(df_cuarentena)} en cuarentena.")

if __name__ == "__main__":
    main()