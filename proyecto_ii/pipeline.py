"""Pipeline: ejecuta en orden la ingesta, el entrenamiento, la inferencia y la explicacion."""

import argparse
import logging

from cliente_ia import ErrorClienteIA, explicar_prediccion
from entrenamiento import COLUMNAS_SIN_CLIMA, ejecutar_entrenamiento
from ingesta import RUTA_SALIDA, ejecutar_ingesta
from procesamiento import ejecutar_inferencia

logger = logging.getLogger(__name__)


def explicar_ejemplo(df, proveedor):
    """Coge a la primera persona de la tabla y pide una explicacion de su prediccion."""
    persona = df.iloc[0]
    habitos = persona[COLUMNAS_SIN_CLIMA].to_dict()
    try:
        explicacion = explicar_prediccion(
            habitos, persona["prediccion"], persona["confianza"], proveedor=proveedor
        )
    except ErrorClienteIA as error:
        # si falla la API del modelo no tiramos todo el pipeline, lo avisamos y seguimos
        logger.warning("No se pudo generar la explicacion: %s", error)
        return None

    logger.info("Explicacion para %s (%s, modelo %s): %s",
                persona["user_id"], explicacion.proveedor, explicacion.modelo, explicacion.texto)
    return explicacion


def ejecutar_pipeline(descargar=True, proveedor="mock"):
    """Lanza los cuatro pasos seguidos. Si descargar es False no llama a la API del clima."""
    logger.info("Paso 1 de 4: ingesta")
    if descargar:
        ejecutar_ingesta()
    else:
        logger.info("Se salta la descarga, se usa la tabla que ya hay en %s", RUTA_SALIDA)

    logger.info("Paso 2 de 4: entrenamiento")
    metricas = ejecutar_entrenamiento()

    logger.info("Paso 3 de 4: inferencia")
    df = ejecutar_inferencia()

    logger.info("Paso 4 de 4: explicacion con %s", proveedor)
    explicacion = explicar_ejemplo(df, proveedor)

    logger.info("Pipeline terminado")
    return metricas, df, explicacion


if __name__ == "__main__":
    # argparse sirve para leer opciones que se escriben al lanzar el comando
    parser = argparse.ArgumentParser(description="Pipeline del Proyecto II")
    parser.add_argument(
        "--sin-descarga",
        action="store_true",
        help="no llama a la API del clima, usa la tabla que ya esta guardada",
    )
    parser.add_argument(
        "--proveedor",
        default="mock",
        choices=["mock", "nvidia"],
        help="quien explica la prediccion: mock (sin internet) o nvidia (API de NVIDIA)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ejecutar_pipeline(descargar=not args.sin_descarga, proveedor=args.proveedor)
