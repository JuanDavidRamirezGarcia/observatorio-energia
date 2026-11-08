from src import config
from src import transformar


def test_main_completa_bronce_limpia_y_construye_en_orden(monkeypatch):
    llamadas = []

    for nombre in ("xm", "ideam", "noaa", "enerandes", "trm"):
        extractor = getattr(transformar, nombre)
        monkeypatch.setattr(
            extractor,
            "extraer",
            lambda nombre=nombre: llamadas.append(f"extraer_{nombre}"),
        )

    for nombre in (
        "limpiar_enerandes",
        "limpiar_noaa",
        "limpiar_xm",
        "limpiar_ideam",
        "limpiar_trm",
    ):
        monkeypatch.setattr(
            transformar,
            nombre,
            lambda nombre=nombre: llamadas.append(nombre),
        )

    def ejecutar_dbt(comando, *, cwd, check):
        llamadas.append(("dbt", comando, cwd, check))

    monkeypatch.setattr(transformar.subprocess, "run", ejecutar_dbt)

    transformar.main()

    assert llamadas == [
        "extraer_xm",
        "extraer_ideam",
        "extraer_noaa",
        "extraer_enerandes",
        "extraer_trm",
        "limpiar_enerandes",
        "limpiar_noaa",
        "limpiar_xm",
        "limpiar_ideam",
        "limpiar_trm",
        (
            "dbt",
            ["dbt", "build", "--project-dir", "dbt", "--profiles-dir", "dbt"],
            config.RAIZ,
            True,
        ),
    ]
