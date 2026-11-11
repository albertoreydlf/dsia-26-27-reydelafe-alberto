"""Pipeline: ejecuta en orden la ingesta, el entrenamiento y la inferencia."""

import argparse
import logging

from entrenamiento import ejecutar_entrenamiento
from ingesta import RUTA_SALIDA, ejecutar_ingesta
from procesamiento import ejecutar_inferencia

logger = logging.getLogger(__name__)


def ejecutar_pipeline(descargar=True):
    """Lanza los tres pasos seguidos. Si descargar es False no llama a la API del clima."""
    logger.info("Paso 1 de 3: ingesta")
    if descargar:
        ejecutar_ingesta()
    else:
        logger.info("Se salta la descarga, se usa la tabla que ya hay en %s", RUTA_SALIDA)

    logger.info("Paso 2 de 3: entrenamiento")
    metricas = ejecutar_entrenamiento()

    logger.info("Paso 3 de 3: inferencia")
    df = ejecutar_inferencia()

    logger.info("Pipeline terminado")
    return metricas, df


if __name__ == "__main__":
    # argparse sirve para leer opciones que se escriben al lanzar el comando
    parser = argparse.ArgumentParser(description="Pipeline del Proyecto II")
    parser.add_argument(
        "--sin-descarga",
        action="store_true",
        help="no llama a la API del clima, usa la tabla que ya esta guardada",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ejecutar_pipeline(descargar=not args.sin_descarga)
