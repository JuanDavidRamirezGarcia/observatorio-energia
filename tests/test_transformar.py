from src import config
from src import transformar


def test_main_limpia_fuentes_antes_de_ejecutar_dbt(monkeypatch):
    llamadas = []

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
