"""Procesamiento: carga el modelo guardado y predice la categoria de deuda de sueno."""

import logging
from pathlib import Path

import joblib
import pandas as pd

from entrenamiento import COLUMNAS_CON_CLIMA, RUTA_MODELO
from ingesta import CARPETA_DATOS, RUTA_SALIDA

logger = logging.getLogger(__name__)

RUTA_PREDICCIONES = CARPETA_DATOS / "predicciones.csv"


def cargar_modelo(ruta=RUTA_MODELO):
    """Carga el modelo que guardo el entrenamiento."""
    if not Path(ruta).exists():
        raise FileNotFoundError(f"No existe el modelo en {ruta}, ejecuta antes entrenamiento.py")
    modelo = joblib.load(ruta)
    logger.info("Modelo cargado de %s", ruta)
    return modelo


def predecir(modelo, df):
    """Devuelve la misma tabla con dos columnas nuevas: prediccion y confianza."""
    # comprobamos que estan todas las columnas con las que se entreno el modelo
    faltan = [columna for columna in COLUMNAS_CON_CLIMA if columna not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas para predecir: {faltan}")

    X = df[COLUMNAS_CON_CLIMA]
    df = df.copy()
    df["prediccion"] = modelo.predict(X)
    # predict_proba da la probabilidad de cada categoria, nos quedamos con la mas alta
    # sirve para saber como de seguro esta el modelo de lo que dice
    df["confianza"] = modelo.predict_proba(X).max(axis=1).round(3)
    return df


def ejecutar_inferencia(ruta_datos=RUTA_SALIDA, ruta_predicciones=RUTA_PREDICCIONES):
    """Carga el modelo, predice para toda la tabla y guarda las predicciones."""
    modelo = cargar_modelo()
    df = pd.read_csv(ruta_datos)
    df = predecir(modelo, df)

    columnas = ["user_id", "ciudad", "fecha", "prediccion", "confianza"]
    df[columnas].to_csv(ruta_predicciones, index=False)
    logger.info("Guardadas %d predicciones en %s", len(df), ruta_predicciones)
    logger.info("Reparto de predicciones: %s", df["prediccion"].value_counts().to_dict())
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ejecutar_inferencia()
