"""Ingesta: lee el CSV del sueno, le anade el clima de Open-Meteo y guarda la tabla unida."""

import logging
from pathlib import Path

import numpy as np
import pandas as pd
import requests

logger = logging.getLogger(__name__)

CARPETA_DATOS = Path(__file__).parent / "data"
RUTA_SUENO = CARPETA_DATOS / "bedtime_screentime_sleep_debt.csv"
RUTA_SALIDA = CARPETA_DATOS / "sueno_con_clima.csv"

# el endpoint de la API historica de Open-Meteo (no pide clave)
URL_CLIMA = "https://archive-api.open-meteo.com/v1/archive"
FECHA_INICIO = "2025-01-01"
FECHA_FIN = "2025-12-31"
SEMILLA = 42

# latitud y longitud de cada ciudad, la API funciona con coordenadas
CIUDADES = {
    "Madrid": (40.4168, -3.7038),
    "Barcelona": (41.3874, 2.1686),
    "Sevilla": (37.3891, -5.9845),
    "Las Palmas de Gran Canaria": (28.1235, -15.4363),
    "Santa Cruz de Tenerife": (28.4636, -16.2518),
}

# variables diarias que pedimos, con el nombre exacto que usa la API
VARIABLES_CLIMA = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "daylight_duration",
    "relative_humidity_2m_mean",
    "surface_pressure_mean",
    "cloud_cover_mean",
    "wind_speed_10m_max",
]


def cargar_sueno(ruta=RUTA_SUENO):
    """Lee el CSV del sueno y lo devuelve como tabla."""
    df = pd.read_csv(ruta)
    logger.info("Leidas %d filas del CSV del sueno", len(df))
    return df


def asignar_ciudad_y_fecha(df, semilla=SEMILLA):
    """Le pone a cada persona una ciudad y una fecha al azar (dato sintetico)."""
    # el CSV no trae ni ciudad ni fecha, asi que las sorteamos
    # con la semilla fija el sorteo sale siempre igual
    rng = np.random.default_rng(semilla)
    fechas = pd.date_range(FECHA_INICIO, FECHA_FIN).strftime("%Y-%m-%d")

    df = df.copy()
    df["ciudad"] = rng.choice(list(CIUDADES), size=len(df))
    df["fecha"] = rng.choice(fechas, size=len(df))
    logger.info("Asignada ciudad y fecha a %d filas", len(df))
    return df


def descargar_clima_ciudad(ciudad, latitud, longitud):
    """Pide a Open-Meteo el clima diario de una ciudad para todo el rango de fechas."""
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "start_date": FECHA_INICIO,
        "end_date": FECHA_FIN,
        "daily": ",".join(VARIABLES_CLIMA),
        "timezone": "auto",
    }
    try:
        respuesta = requests.get(URL_CLIMA, params=parametros, timeout=30)
        respuesta.raise_for_status()  # salta si la API contesta con un error
    except requests.RequestException as error:
        logger.error("Fallo la API del clima para %s: %s", ciudad, error)
        raise RuntimeError(f"No se pudo descargar el clima de {ciudad}") from error

    # la respuesta trae un bloque "daily" con una lista por cada variable
    clima = pd.DataFrame(respuesta.json()["daily"])
    clima = clima.rename(columns={"time": "fecha"})
    clima["ciudad"] = ciudad
    logger.info("Clima descargado de %s: %d dias", ciudad, len(clima))
    return clima


def descargar_clima():
    """Descarga el clima de todas las ciudades y lo junta en una sola tabla."""
    tablas = []
    for ciudad, (latitud, longitud) in CIUDADES.items():
        tablas.append(descargar_clima_ciudad(ciudad, latitud, longitud))
    return pd.concat(tablas, ignore_index=True)


def unir(df_sueno, df_clima):
    """Pega a cada persona el clima de su ciudad y su fecha (el join)."""
    # how="left" es para quedarnos con todas las personas aunque faltase su clima
    df = df_sueno.merge(df_clima, on=["ciudad", "fecha"], how="left")

    sin_clima = df[VARIABLES_CLIMA[0]].isna().sum()
    if sin_clima > 0:
        logger.warning("Hay %d filas que se quedaron sin clima", sin_clima)
    return df


def ejecutar_ingesta(ruta_salida=RUTA_SALIDA):
    """Hace toda la ingesta en orden y guarda la tabla final."""
    df_sueno = cargar_sueno()
    df_sueno = asignar_ciudad_y_fecha(df_sueno)
    df_clima = descargar_clima()
    df = unir(df_sueno, df_clima)

    df.to_csv(ruta_salida, index=False)
    logger.info("Guardada la tabla con clima en %s (%d filas, %d columnas)",
                ruta_salida, df.shape[0], df.shape[1])
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ejecutar_ingesta()
