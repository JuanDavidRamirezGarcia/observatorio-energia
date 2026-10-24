from datetime import date

from src import config
from src.extract import xm
from src.utils import ventanas


def test_ventanas_parte_rango_en_bloques_inclusivos():
    resultado = list(
        ventanas(date(2026, 1, 1), date(2026, 1, 10), dias=4)
    )

    assert resultado == [
        (date(2026, 1, 1), date(2026, 1, 4)),
        (date(2026, 1, 5), date(2026, 1, 8)),
        (date(2026, 1, 9), date(2026, 1, 10)),
    ]


def test_ventanas_incluye_un_rango_de_un_solo_dia():
    dia = date(2026, 1, 1)

    assert list(ventanas(dia, dia, dias=30)) == [(dia, dia)]


def test_aplanar_convierte_entidades_horarias():
    respuesta = {
        "Items": [
            {
                "Date": "2026-01-01",
                "HourlyEntities": [
                    {"Id": "Sistema", "Values": {"Hour01": "10.5", "Hour02": "11"}}
                ],
            }
        ]
    }

    assert xm.aplanar(respuesta, "hourly") == [
        {
            "Date": "2026-01-01",
            "Id": "Sistema",
            "Hour01": "10.5",
            "Hour02": "11",
        }
    ]


def test_aplanar_convierte_entidades_diarias():
    respuesta = {
        "Items": [
            {
                "Date": "2026-01-01",
                "DailyEntities": [{"Id": "Sistema", "Value": "0.7"}],
            }
        ]
    }

    assert xm.aplanar(respuesta, "daily") == [
        {"Date": "2026-01-01", "Id": "Sistema", "Value": "0.7"}
    ]


def test_aplanar_conserva_entidades_de_listado():
    entidad = {"Id": "Recurso1", "Name": "Recurso"}
    respuesta = {"Items": [{"ListEntities": [entidad]}]}

    assert xm.aplanar(respuesta, "lists") == [entidad]


def test_extraer_metrica_omite_archivo_existente(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DIR_BRONZE", tmp_path)
    (tmp_path / "xm_demanda.parquet").touch()

    def no_debe_llamarse(*args, **kwargs):
        raise AssertionError("No se debe descargar ni guardar un archivo existente")

    monkeypatch.setattr(xm, "http_json", no_debe_llamarse)
    monkeypatch.setattr(xm, "guardar_bronce", no_debe_llamarse)

    xm.extraer_metrica(
        metrica="DemaReal",
        entidad="Sistema",
        periodo="hourly",
        nombre="xm_demanda",
        forzar=False,
    )
