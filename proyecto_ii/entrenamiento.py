"""Entrenamiento: entrena el modelo de scikit-learn, lo mide y lo guarda con joblib."""

import json
import logging
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from ingesta import RUTA_SALIDA, VARIABLES_CLIMA

logger = logging.getLogger(__name__)

CARPETA_MODELOS = Path(__file__).parent / "models"
RUTA_MODELO = CARPETA_MODELOS / "modelo.joblib"
RUTA_METRICAS = CARPETA_MODELOS / "metricas.json"
SEMILLA = 42

# lo que queremos predecir
OBJETIVO = "sleep_debt_category"

# solo usamos cosas que se saben ANTES de dormir
# no metemos total_sleep_hours ni parecidas porque con eso el modelo "copia" la respuesta
COLUMNAS_NUMERICAS = [
    "age",
    "bedtime_phone_minutes",
    "screen_brightness_pct",
    "blue_light_filter_active",
    "caffeine_post_5pm_mg",
    "physical_activity_min",
]
COLUMNAS_TEXTO = ["gender", "occupation_type", "chronotype", "primary_bedtime_app"]

COLUMNAS_SIN_CLIMA = COLUMNAS_NUMERICAS + COLUMNAS_TEXTO
COLUMNAS_CON_CLIMA = COLUMNAS_SIN_CLIMA + VARIABLES_CLIMA


def cargar_datos(ruta=RUTA_SALIDA):
    """Lee la tabla que dejo la ingesta (sueno + clima)."""
    df = pd.read_csv(ruta)
    logger.info("Leidas %d filas para entrenar", len(df))
    return df


def dividir_datos(df):
    """Parte los datos en train (70%), validacion (15%) y test (15%)."""
    # stratify hace que las 4 categorias salgan en la misma proporcion en cada parte
    df_train, df_resto = train_test_split(
        df, test_size=0.30, random_state=SEMILLA, stratify=df[OBJETIVO]
    )
    # el 30% que sobra lo partimos por la mitad: 15% validacion y 15% test
    df_val, df_test = train_test_split(
        df_resto, test_size=0.50, random_state=SEMILLA, stratify=df_resto[OBJETIVO]
    )
    logger.info("Reparto: train=%d, validacion=%d, test=%d",
                len(df_train), len(df_val), len(df_test))
    return df_train, df_val, df_test


def crear_modelo():
    """Crea el pipeline: primero prepara las columnas y despues va el random forest."""
    # las columnas de texto se pasan a numeros (una columna de 0/1 por cada valor)
    # handle_unknown="ignore" es para que no falle si llega un valor que no vio al entrenar
    # remainder="passthrough" deja las columnas numericas como estan
    preparar = ColumnTransformer(
        [("texto", OneHotEncoder(handle_unknown="ignore"), COLUMNAS_TEXTO)],
        remainder="passthrough",
    )
    bosque = RandomForestClassifier(
        n_estimators=100, min_samples_leaf=5, random_state=SEMILLA
    )
    return Pipeline([("preparar", preparar), ("bosque", bosque)])


def entrenar(df_train, columnas):
    """Entrena un modelo usando solo las columnas que le digamos."""
    modelo = crear_modelo()
    modelo.fit(df_train[columnas], df_train[OBJETIVO])
    return modelo


def evaluar(modelo, df, columnas):
    """Calcula accuracy y f1 macro del modelo sobre los datos que le pasemos."""
    predicciones = modelo.predict(df[columnas])
    return {
        "accuracy": round(accuracy_score(df[OBJETIVO], predicciones), 4),
        "f1_macro": round(f1_score(df[OBJETIVO], predicciones, average="macro"), 4),
    }


def ejecutar_entrenamiento(ruta_modelo=RUTA_MODELO, ruta_metricas=RUTA_METRICAS):
    """Entrena, compara sin clima y con clima, y guarda el modelo y las metricas."""
    df = cargar_datos()
    df_train, df_val, df_test = dividir_datos(df)

    # entrenamos dos modelos con los mismos datos de train
    modelo_sin_clima = entrenar(df_train, COLUMNAS_SIN_CLIMA)
    modelo_con_clima = entrenar(df_train, COLUMNAS_CON_CLIMA)

    # los comparamos en validacion (el test todavia no se toca)
    val_sin_clima = evaluar(modelo_sin_clima, df_val, COLUMNAS_SIN_CLIMA)
    val_con_clima = evaluar(modelo_con_clima, df_val, COLUMNAS_CON_CLIMA)
    logger.info("Validacion sin clima: %s", val_sin_clima)
    logger.info("Validacion con clima: %s", val_con_clima)

    # nos quedamos con el de clima, que es el que usa todo el pipeline
    # el test se usa una sola vez, al final, para dar la nota definitiva
    test_final = evaluar(modelo_con_clima, df_test, COLUMNAS_CON_CLIMA)
    clases = list(modelo_con_clima.classes_)
    matriz = confusion_matrix(
        df_test[OBJETIVO], modelo_con_clima.predict(df_test[COLUMNAS_CON_CLIMA]), labels=clases
    )
    logger.info("Test del modelo final: %s", test_final)

    # referencia: lo que acertariamos diciendo siempre la categoria mas comun
    acierto_sin_modelo = round(df_test[OBJETIVO].value_counts(normalize=True).max(), 4)

    metricas = {
        "reparto": {"train": len(df_train), "validacion": len(df_val), "test": len(df_test)},
        "validacion": {"sin_clima": val_sin_clima, "con_clima": val_con_clima},
        "test_modelo_final": test_final,
        "acierto_diciendo_siempre_la_mas_comun": acierto_sin_modelo,
        "clases": clases,
        "matriz_confusion_test": matriz.tolist(),
    }

    joblib.dump(modelo_con_clima, ruta_modelo, compress=3)
    with open(ruta_metricas, "w") as fichero:
        json.dump(metricas, fichero, indent=2)
    logger.info("Modelo guardado en %s", ruta_modelo)
    logger.info("Metricas guardadas en %s", ruta_metricas)
    return metricas


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ejecutar_entrenamiento()
