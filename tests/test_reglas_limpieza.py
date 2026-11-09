import pandas as pd
import pytest

from src.silver.enerandes import limpiar_hoja, estandarizar_fecha, normalizar_segmento, normalizar_tipo_compra
from src.silver.noaa import calcular_fase_enso
from src.silver.xm import unpivot_24_horas


def test_estandarizar_fecha_reconoce_mar_24():
    assert estandarizar_fecha("mar-24") == "2024-03"


def test_estandarizar_fecha_reconoce_formato_dd_mm_yyyy():
    assert estandarizar_fecha("03/2024") == "2024-03"


def test_limpiar_hoja_2024_convierte_mwh_a_kwh():
    df = pd.DataFrame(
        {
            "periodo": ["01/2024", "02/2024"],
            "municipio": ["Medellín", "Bello"],
            "segmento": ["Residencial", "Comercial"],
            "tipo_compra": ["Bolsa", "Contrato"],
            "energia_kwh": ["10", "5"],
            "valor_cop": ["50000", "75000"],
            "clientes": ["10", "8"],
        }
    )

    limpias, cuarentena = limpiar_hoja(df, 2024)

    assert cuarentena.empty
    assert limpias["energia_kwh"].tolist() == [10000.0, 5000.0]
    assert limpias["valor_cop"].tolist() == [50000.0, 75000.0]


@pytest.mark.parametrize(
    "oni, esperado",
    [
        (0.6, "El Niño"),
        (-0.8, "La Niña"),
        (0.2, "Neutral"),
    ],
)
def test_calcular_fase_enso_segun_valor_oni(oni, esperado):
    assert calcular_fase_enso(oni) == esperado


def test_normalizar_segmento_y_tipo_compra_resuelven_aliases():
    assert normalizar_segmento("residencial") == "Residencial"
    assert normalizar_segmento("Comercial ") == "Comercial"
    assert normalizar_tipo_compra("bolsa") == "Bolsa"
    assert normalizar_tipo_compra("contrato") == "Contrato"


def test_unpivot_24_horas_generates_one_row_per_hour():
    horas = {f"Hour{i:02d}": [float(i)] for i in range(1, 25)}
    df = pd.DataFrame(
        {
            "Date": ["2026-01-01"],
            "Id": ["Sistema"],
            "code": ["DEM"],
            **horas,
        }
    )

    resultado = unpivot_24_horas(df, "demanda_kwh")

    assert len(resultado) == 24
    assert resultado["hora"].tolist() == list(range(1, 25))
    assert resultado["demanda_kwh"].tolist() == [float(i) for i in range(1, 25)]
    assert resultado["fecha"].dt.strftime("%Y-%m-%d").nunique() == 1
