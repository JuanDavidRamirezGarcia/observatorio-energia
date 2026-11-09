from datetime import date

import pandas as pd

from src import config
from src import pipeline
from src.extract import ideam
from src.extract import xm
from src.pipeline import generar_muestras
from src.utils import ventanas


def test_configura_metricas_xm_nuevas():
    metricas = set(config.XM_METRICAS)

    assert {
        ("Gene", "Recurso", "hourly", "xm_generacion"),
        ("AporEner", "Sistema", "daily", "xm_aportes"),
        ("ListadoRecursos", "", "lists", "xm_listado_recursos"),
    } <= metricas


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


def test_generar_muestras_exporta_las_primeras_200_filas(tmp_path, monkeypatch):
    dir_bronze = tmp_path / "bronze"
    dir_sample = tmp_path / "sample"
    dir_bronze.mkdir()
    monkeypatch.setattr(config, "DIR_BRONZE", dir_bronze)
    monkeypatch.setattr(config, "DIR_SAMPLE", dir_sample)

    datos = pd.DataFrame({"valor": range(250)})
    datos.to_parquet(dir_bronze / "fuente.parquet", index=False)
    pocos_datos = pd.DataFrame({"valor": range(50)})
    pocos_datos.to_parquet(dir_bronze / "fuente_corta.parquet", index=False)

    generar_muestras()

    muestra = pd.read_csv(dir_sample / "fuente_sample.csv")
    assert len(muestra) == 200
    assert muestra["valor"].tolist() == list(range(200))
    muestra_corta = pd.read_csv(dir_sample / "fuente_corta_sample.csv")
    assert muestra_corta["valor"].tolist() == list(range(50))


def test_pipeline_desde_carpetas_vacias_genera_muestras_de_todas_las_fuentes(
    tmp_path, monkeypatch
):
    dir_bronze = tmp_path / "bronze"
    dir_sample = tmp_path / "sample"
    monkeypatch.setattr(config, "DIR_BRONZE", dir_bronze)
    monkeypatch.setattr(config, "DIR_SAMPLE", dir_sample)
    monkeypatch.setattr(pipeline.sys, "argv", ["python", "-m", "src.pipeline"])

    extractores = (
        pipeline.xm,
        pipeline.ideam,
        pipeline.noaa,
        pipeline.enerandes,
        pipeline.trm,
    )
    nombres = ("xm", "ideam", "noaa", "enerandes", "trm")
    llamadas = []

    def crear_stub(nombre):
        def extraer(forzar=False):
            llamadas.append((nombre, forzar))
            dir_bronze.mkdir(parents=True, exist_ok=True)
            pd.DataFrame({"valor": range(205)}).to_parquet(
                dir_bronze / f"{nombre}.parquet", index=False
            )

        return extraer

    for extractor, nombre in zip(extractores, nombres):
        monkeypatch.setattr(extractor, "extraer", crear_stub(nombre))

    pipeline.main()

    assert llamadas == [(nombre, False) for nombre in nombres]
    for nombre in nombres:
        muestra = pd.read_csv(dir_sample / f"{nombre}_sample.csv")
        assert muestra["valor"].tolist() == list(range(200))


def test_ideam_recorre_todo_el_ano_2025(monkeypatch):
    ventanas_procesadas = []

    monkeypatch.setattr(ideam, "ya_existe", lambda nombre, forzar: False)
    monkeypatch.setattr(
        ideam,
        "http_json",
        lambda metodo, url, params: ventanas_procesadas.append(params) or [],
    )
    monkeypatch.setattr(ideam, "guardar_bronce", lambda *args, **kwargs: None)
    monkeypatch.setattr(config, "IDEAM_FECHA_INICIO", date(2025, 1, 1))
    monkeypatch.setattr(config, "IDEAM_FECHA_FIN", date(2025, 12, 31))
    monkeypatch.setattr(config, "IDEAM_DIAS_VENTANA", 7)

    ideam._extraer_dataset_ideam(
        "ideam_prueba",
        "https://example.test/ideam",
        ideam.consulta_soql_precipitacion,
    )

    assert len(ventanas_procesadas) == 53
    assert "2025-01-01T00:00:00" in ventanas_procesadas[0]["$where"]
    assert "2025-12-31T23:59:59" in ventanas_procesadas[-1]["$where"]
