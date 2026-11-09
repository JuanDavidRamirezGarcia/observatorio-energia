"""
Reglas de calidad de la capa plata escritas con pandera.
Define los esquemas para validar cada tabla que se guarda en la capa plata.
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

# 3. Esquemas de XM (precio, demanda y embalses)
ESQUEMA_XM_PRECIO_BOLSA = pa.DataFrameSchema(
    {
        "Date": Column(pa.DateTime, nullable=False),
        "Id": Column(str, nullable=False),
        "code": Column(str, nullable=False),
        "hora_str": Column(str, nullable=False),
        "hora": Column(int, Check.in_range(min_value=1, max_value=24), nullable=False),
        "fecha": Column(pa.DateTime, nullable=False),
        "precio_bolsa_kwh": Column(float, Check.ge(0), nullable=False),
    },
    unique=["Date", "Id", "code", "hora"],
    strict=False,
)

ESQUEMA_XM_DEMANDA = pa.DataFrameSchema(
    {
        "Date": Column(pa.DateTime, nullable=False),
        "Id": Column(str, nullable=False),
        "code": Column(str, nullable=False),
        "hora_str": Column(str, nullable=False),
        "hora": Column(int, Check.in_range(min_value=1, max_value=24), nullable=False),
        "fecha": Column(pa.DateTime, nullable=False),
        "demanda_kwh": Column(float, Check.ge(0), nullable=False),
    },
    unique=["Date", "Id", "code", "hora"],
    strict=False,
)

ESQUEMA_XM_EMBALSES = pa.DataFrameSchema(
    {
        "Date": Column(pa.DateTime, nullable=False),
        "Id": Column(str, nullable=False),
        "Value": Column(float, Check.ge(0), nullable=False),
    },
    unique=["Date", "Id"],
    strict=False,
)

# 4. Esquemas de IDEAM (precipitación y temperatura)
ESQUEMA_IDEAM_PRECIPITACION = pa.DataFrameSchema(
    {
        "fecha": Column(pa.DateTime, nullable=False),
        "codigoestacion": Column(str, nullable=False),
        "nombreestacion": Column(str, nullable=False),
        "municipio": Column(str, nullable=False),
        "latitud": Column(float, Check.in_range(min_value=-90, max_value=90), nullable=True),
        "longitud": Column(float, Check.in_range(min_value=-180, max_value=180), nullable=True),
        "precipitacion_mm": Column(float, Check.ge(0), nullable=False),
        "n_obs": Column(int, Check.ge(0), nullable=True),
    },
    unique=["fecha", "codigoestacion"],
    strict=False,
)

ESQUEMA_IDEAM_TEMPERATURA = pa.DataFrameSchema(
    {
        "fecha": Column(pa.DateTime, nullable=False),
        "codigoestacion": Column(str, nullable=False),
        "nombreestacion": Column(str, nullable=False),
        "municipio": Column(str, nullable=False),
        "latitud": Column(float, Check.in_range(min_value=-90, max_value=90), nullable=True),
        "longitud": Column(float, Check.in_range(min_value=-180, max_value=180), nullable=True),
        "temperatura_celsius": Column(float, nullable=False),
        "n_obs": Column(int, Check.ge(0), nullable=True),
    },
    unique=["fecha", "codigoestacion"],
    strict=False,
)

# Compatibilidad con nombres previos
ESQUEMA_XM_HORARIO = ESQUEMA_XM_DEMANDA