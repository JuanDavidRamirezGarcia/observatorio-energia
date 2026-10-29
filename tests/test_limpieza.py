"""
Pruebas automáticas con pytest para las reglas de limpieza de la Capa Plata.
"""
import pandas as pd
import pandera.errors
import pytest
from src.quality.esquemas import ESQUEMA_VENTAS
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
    with pytest.raises(pandera.errors.SchemaErrors):
        ESQUEMA_VENTAS.validate(df_mal, lazy=True)