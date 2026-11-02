"""
Reglas de calidad de la capa plata escritas con pandera.
Define los esquemas para validar las tablas de EnerAndes, XM y NOAA antes de guardarlas.
"""
import pandera.pandas as pa
from pandera.pandas import Check, Column

SEGMENTOS = ["Residencial", "Comercial", "Industrial", "No informado"]
TIPOS_COMPRA = ["Bolsa", "Contrato"]
FASES_ENSO = ["El Niño", "La Niña", "Neutral"]

# 1. Esquema de EnerAndes (Ventas consolidadas 2023-2026)
ESQUEMA_VENTAS = pa.DataFrameSchema(
    {
        "periodo": Column(str, Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$")),
        "divipola": Column(str, Check.str_matches(r"^\d{5}$")),
        "municipio": Column(str),
        "segmento": Column(str, Check.isin(SEGMENTOS)),
        "tipo_compra": Column(str, Check.isin(TIPOS_COMPRA)),
        "energia_kwh": Column(float, Check.ge(0)),
        "valor_cop": Column(float, Check.ge(0), nullable=True),
        "clientes": Column(int, Check.ge(0)),
    },
    unique=["periodo", "divipola", "segmento", "tipo_compra"],
    strict=True,
)

# 2. Esquema de NOAA (Índice ONI y Fase ENSO)
ESQUEMA_NOAA = pa.DataFrameSchema(
    {
        "periodo": Column(str, Check.str_matches(r"^\d{4}-(0[1-9]|1[0-2])$")),
        "oni": Column(float),
        "fase_enso": Column(str, Check.isin(FASES_ENSO)),
    },
    unique=["periodo"],
    strict=True,
)

# 3. Esquema de XM Horario (Mercado)
ESQUEMA_XM_HORARIO = pa.DataFrameSchema(
    {
        "fecha": Column(pa.DateTime),
        "hora": Column(int, Check.in_range(1, 24)),
        "valor": Column(float, Check.ge(0)),
    },
    strict=False,
)