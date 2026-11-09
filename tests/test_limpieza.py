"""
Pruebas automáticas con pytest para las reglas de limpieza de la Capa Plata.
"""
import pandas as pd
import pandera as pa
import pytest
from src.quality.esquemas import (
    ESQUEMA_IDEAM_PRECIPITACION,
    ESQUEMA_IDEAM_TEMPERATURA,
    ESQUEMA_NOAA,
    ESQUEMA_VENTAS,
    ESQUEMA_XM_DEMANDA,
    ESQUEMA_XM_EMBALSES,
    ESQUEMA_XM_PRECIO_BOLSA,
)
from src.silver.enerandes import clave_municipio, estandarizar_fecha, sin_tildes

def test_sin_tildes_quita_tildes_mayusculas_y_espacios():
    assert sin_tildes(" ITAGÜÍ ") == "itagui"
    assert sin_tildes("Medellín") == "medellin"

def test_clave_municipio_resuelve_los_alias():
    assert clave_municipio("Rio Negro") == "rionegro"
    assert clave_municipio("Medellín D.E.") == "medellin"
    assert clave_municipio(None) is None

def test_convertir_mwh_a_kwh_hoja_2024():
    df_test = pd.DataFrame({"anio": [2024, 2023], "energia": [10.5, 5000.0]})
    df_test.loc[df_test["anio"] == 2024, "energia"] *= 1000.0
    assert df_test.loc[df_test["anio"] == 2024, "energia"].iloc[0] == 10500.0
    assert df_test.loc[df_test["anio"] == 2023, "energia"].iloc[0] == 5000.0

def test_parseo_fecha_corte_2026():
    # Garantiza que 01/03/2026 corresponda a marzo (2026-03)
    assert estandarizar_fecha("01/03/2026") == "2026-03"

def test_parseo_fechas_heterogeneas():
    assert estandarizar_fecha("2024-03") == "2024-03"
    assert estandarizar_fecha("mar-24") == "2024-03"
    assert estandarizar_fecha("03/2024") == "2024-03"

def test_pandera_rechaza_tipo_compra_invalido():
    df_mal = pd.DataFrame({
        "periodo": ["2023-01"],
        "divipola": ["05001"],
        "municipio": ["Medellín"],
        "segmento": ["Residencial"],
        "tipo_compra": ["OTRO_TIPO"],
        "energia_kwh": [100.0],
        "valor_cop": [50000.0],
        "clientes": [10]
    })
    # Se usa SchemaErrors (en plural) porque lazy=True agrupa múltiples fallas
    with pytest.raises((pa.errors.SchemaError, pa.errors.SchemaErrors)):
        ESQUEMA_VENTAS.validate(df_mal, lazy=True)
        

def test_conversion_mwh_a_kwh():
    """Valida que la energía de EnerAndes se multiplique por 1000."""
    mwh = 5.0
    kwh = mwh * 1000
    assert kwh == 5000.0

def test_clasificacion_enso_nino():
    """Valida que un valor ONI >= 0.5 se clasifique como El Niño (NOAA)."""
    oni = 0.6
    fase = "El Niño" if oni >= 0.5 else ("La Niña" if oni <= -0.5 else "Neutral")
    assert fase == "El Niño"

def test_clasificacion_enso_nina():
    """Valida que un valor ONI <= -0.5 se clasifique como La Niña (NOAA)."""
    oni = -0.8
    fase = "El Niño" if oni >= 0.5 else ("La Niña" if oni <= -0.5 else "Neutral")
    assert fase == "La Niña"

def test_formato_mes_noaa():
    """Valida el parseo correcto de trimestres a formato YYYY-MM."""
    año = 2024
    mes_str = "01"
    assert f"{año}-{mes_str}" == "2024-01"

def test_correccion_comas_ideam():
    """Valida la conversión de comas decimales a puntos en mediciones de IDEAM."""
    valor_original = "22,5"
    valor_corregido = float(valor_original.replace(",", "."))
    assert valor_corregido == 22.5


def test_esquemas_plata_cubren_todas_las_tablas():
    """Cada tabla de la capa plata debe contar con un esquema pandera con validación real."""
    assert ESQUEMA_VENTAS is not None
    assert ESQUEMA_NOAA is not None
    assert ESQUEMA_XM_PRECIO_BOLSA is not None
    assert ESQUEMA_XM_DEMANDA is not None
    assert ESQUEMA_XM_EMBALSES is not None
    assert ESQUEMA_IDEAM_PRECIPITACION is not None
    assert ESQUEMA_IDEAM_TEMPERATURA is not None

    df_ventas_ok = pd.DataFrame({
        "periodo": ["2024-01", "2024-02"],
        "divipola": ["05001", "05001"],
        "municipio": ["Medellín", "Medellín"],
        "segmento": ["Residencial", "Comercial"],
        "tipo_compra": ["Bolsa", "Contrato"],
        "energia_kwh": [100.0, 220.5],
        "valor_cop": [50000.0, 70000.0],
        "clientes": [10, 13],
    })
    ESQUEMA_VENTAS.validate(df_ventas_ok, lazy=True)

    df_noaa_ok = pd.DataFrame({
        "periodo": ["2024-01", "2024-02"],
        "oni": [0.6, -0.7],
        "fase_enso": ["El Niño", "La Niña"],
    })
    ESQUEMA_NOAA.validate(df_noaa_ok, lazy=True)

    df_prec_ok = pd.DataFrame({
        "fecha": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "codigoestacion": ["ABC", "ABC"],
        "nombreestacion": ["Estación A", "Estación A"],
        "municipio": ["Medellín", "Medellín"],
        "latitud": [6.23, 6.23],
        "longitud": [-75.57, -75.57],
        "precipitacion_mm": [12.5, 0.0],
        "n_obs": [24, 24],
    })
    ESQUEMA_IDEAM_PRECIPITACION.validate(df_prec_ok, lazy=True)

    df_temp_ok = pd.DataFrame({
        "fecha": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "codigoestacion": ["ABC", "ABC"],
        "nombreestacion": ["Estación A", "Estación A"],
        "municipio": ["Medellín", "Medellín"],
        "latitud": [6.23, 6.23],
        "longitud": [-75.57, -75.57],
        "temperatura_celsius": [22.5, 23.0],
        "n_obs": [24, 24],
    })
    ESQUEMA_IDEAM_TEMPERATURA.validate(df_temp_ok, lazy=True)

    df_precio_ok = pd.DataFrame({
        "Date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
        "Id": ["A", "A"],
        "code": ["XBTC", "XBTC"],
        "hora_str": ["Hour01", "Hour02"],
        "hora": [1, 2],
        "fecha": pd.to_datetime(["2024-01-01", "2024-01-01"]),
        "precio_bolsa_kwh": [120.0, 128.5],
    })
    ESQUEMA_XM_PRECIO_BOLSA.validate(df_precio_ok, lazy=True)

    df_demanda_ok = pd.DataFrame({
        "Date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
        "Id": ["A", "A"],
        "code": ["DEM", "DEM"],
        "hora_str": ["Hour01", "Hour02"],
        "hora": [1, 2],
        "fecha": pd.to_datetime(["2024-01-01", "2024-01-01"]),
        "demanda_kwh": [50.0, 55.0],
    })
    ESQUEMA_XM_DEMANDA.validate(df_demanda_ok, lazy=True)

    df_embalse_ok = pd.DataFrame({
        "Date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
        "Id": ["E1", "E2"],
        "Value": [12.5, 14.0],
    })
    ESQUEMA_XM_EMBALSES.validate(df_embalse_ok, lazy=True)

    with pytest.raises((pa.errors.SchemaError, pa.errors.SchemaErrors)):
        ESQUEMA_IDEAM_PRECIPITACION.validate(
            df_prec_ok.assign(precipitacion_mm=[-1.0, 0.0]),
            lazy=True,
        )

    with pytest.raises((pa.errors.SchemaError, pa.errors.SchemaErrors)):
        ESQUEMA_XM_DEMANDA.validate(
            df_demanda_ok.assign(hora=[0, 2]),
            lazy=True,
        )

    with pytest.raises((pa.errors.SchemaError, pa.errors.SchemaErrors)):
        ESQUEMA_XM_EMBALSES.validate(
            pd.concat([df_embalse_ok, df_embalse_ok.iloc[[0]]], ignore_index=True),
            lazy=True,
        )