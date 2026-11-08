"""
Orquestador de datos que completa Bronce, limpia las fuentes y construye Plata y Oro.
"""
import subprocess

from src import config
from src.extract import enerandes, ideam, noaa, trm, xm
from src.silver.enerandes import main as limpiar_enerandes
from src.silver.noaa import main as limpiar_noaa
from src.silver.xm import main as limpiar_xm
from src.silver.ideam import main as limpiar_ideam
from src.silver.trm import main as limpiar_trm
from src.utils import log


def main():
    log("=== VERIFICANDO Y DESCARGANDO INSUMOS BRONCE FALTANTES ===")
    for extractor in (xm, ideam, noaa, enerandes, trm):
        extractor.extraer()

    log("=== INICIANDO PIPELINE DE LIMPIEZA - CAPA PLATA ===")

    log("--- Step 1: EnerAndes (Limpieza y Cuarentena) ---")
    limpiar_enerandes()

    log("--- Step 2: NOAA (Índice ONI / ENSO) ---")
    limpiar_noaa()

    log("--- Step 3: XM (Precio de Bolsa, Demanda, Embalses) ---")
    limpiar_xm()

    log("--- Step 4: IDEAM (Precipitación y Temperatura) ---")
    limpiar_ideam()

    log("--- Step 5: TRM (Fuente propia) ---")
    limpiar_trm()

    log("=== CAPA PLATA COMPLETADA CON ÉXITO ===")
    log("=== INICIANDO CONSTRUCCIÓN DE CAPA ORO CON DBT ===")
    subprocess.run(
        ["dbt", "build", "--project-dir", "dbt", "--profiles-dir", "dbt"],
        cwd=config.RAIZ,
        check=True,
    )
    log("=== CAPA ORO COMPLETADA CON ÉXITO ===")

if __name__ == "__main__":
    main()
