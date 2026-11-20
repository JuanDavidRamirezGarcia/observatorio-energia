from pathlib import Path

import duckdb
import pandas as pd

from src import config


CONSULTAS_ORO = config.RAIZ / "consultas" / "oro"


def ejecutar_consulta(con, nombre: str):
    sql = (CONSULTAS_ORO / nombre).read_text(encoding="utf-8")
    return con.execute(sql).fetchall()


def test_ventas_por_municipio_calcula_consumo_en_gwh():
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE dim_municipio (municipio_id INTEGER, municipio VARCHAR)"
    )
    con.execute(
        "INSERT INTO dim_municipio VALUES (1, 'Medellín'), (2, 'Bello')"
    )
    con.execute(
        "CREATE TABLE fact_ventas_mensual "
        "(municipio_id INTEGER, energia_kwh DOUBLE)"
    )
    con.execute(
        "INSERT INTO fact_ventas_mensual VALUES "
        "(1, 1500000), (1, 500000), (2, 3000000)"
    )

    resultado = ejecutar_consulta(con, "consulta_1_ventas_por_municipio.sql")

    assert resultado == [("Bello", 3.0), ("Medellín", 2.0)]
    con.close()


def test_precio_promedio_por_hora_y_fase_enso(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    ruta_oni = Path("data") / "silver" / "noaa_oni.parquet"
    ruta_oni.parent.mkdir(parents=True)
    pd.DataFrame(
        {"periodo": ["2024-01"], "fase_enso": ["El Niño"]}
    ).to_parquet(ruta_oni, index=False)

    con = duckdb.connect()
    con.execute("CREATE TABLE dim_fecha (fecha_key INTEGER, fase_enso VARCHAR)")
    con.execute("INSERT INTO dim_fecha VALUES (1, 'El Niño'), (2, 'La Niña')")
    con.execute(
        "CREATE TABLE fact_mercado_horario "
        "(fecha_key INTEGER, hora INTEGER, precio_bolsa_kwh DOUBLE)"
    )
    con.execute(
        "INSERT INTO fact_mercado_horario VALUES "
        "(1, 8, 100), (1, 8, 200), (2, 8, 300), (2, 9, 500)"
    )

    resultado = ejecutar_consulta(
        con, "consulta_2_comportamiento_precio_bolsa.sql"
    )

    assert resultado == [
        (8, "El Niño", 150.0),
        (8, "La Niña", 300.0),
        (9, "La Niña", 500.0),
    ]
    con.close()


def test_generacion_vs_demanda_calcula_diferencia_mwh():
    con = duckdb.connect()
    con.execute(
        "CREATE TABLE fact_generacion_recurso "
        "(fecha_key INTEGER, hora INTEGER, generacion_kwh DOUBLE)"
    )
    con.execute(
        "INSERT INTO fact_generacion_recurso VALUES "
        "(1, 8, 10000000), (2, 8, 20000000), "
        "(1, 9, 5000000), (2, 9, 9000000)"
    )
    con.execute(
        "CREATE TABLE fact_mercado_horario "
        "(fecha_key INTEGER, hora INTEGER, demanda_kwh DOUBLE)"
    )
    con.execute(
        "INSERT INTO fact_mercado_horario VALUES "
        "(1, 8, 8000000), (2, 8, 12000000), "
        "(1, 9, 6000000), (2, 9, 10000000)"
    )

    resultado = ejecutar_consulta(
        con, "consulta_3_generacion_vs_demanda.sql"
    )

    assert resultado == [(8, 15.0, 10.0, 5.0), (9, 7.0, 8.0, -1.0)]
    con.close()
