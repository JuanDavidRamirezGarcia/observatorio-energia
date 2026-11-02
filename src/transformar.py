"""
Orquestador general del pipeline de transformación - Capa Plata (Puntos 1 a 4).
Ejecuta la limpieza y estandarización de todas las fuentes de datos.
"""
from src.silver.enerandes import main as limpiar_enerandes
from src.silver.noaa import main as limpiar_noaa
from src.silver.xm import main as limpiar_xm
from src.silver.ideam import main as limpiar_ideam
from src.utils import log

def main():
    log("=== INICIANDO PIPELINE DE LIMPIEZA - CAPA PLATA ===")
    
    log("--- Step 1: EnerAndes (Limpieza y Cuarentena) ---")
    limpiar_enerandes()
    
    log("--- Step 2: NOAA (Índice ONI / ENSO) ---")
    limpiar_noaa()
    
    log("--- Step 3: XM (Precio de Bolsa, Demanda, Embalses) ---")
    limpiar_xm()
    
    log("--- Step 4: IDEAM (Precipitación y Temperatura) ---")
    limpiar_ideam()
    
    log("=== CAPA PLATA COMPLETADA CON ÉXITO ===")

if __name__ == "__main__":
    main()