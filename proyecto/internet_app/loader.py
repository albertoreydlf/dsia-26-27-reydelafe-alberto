import pandas as pd
from pathlib import Path

# Columnas que debe tener el CSV para poder trabajar con él
COLUMNAS_REQUERIDAS = [
    "user_id", "age", "gender", "occupation_type", "chronotype",
    "bedtime_phone_minutes", "primary_bedtime_app", "screen_brightness_pct",
    "blue_light_filter_active", "caffeine_post_5pm_mg", "physical_activity_min",
    "sleep_latency_min", "total_sleep_hours", "deep_sleep_pct", "rem_sleep_pct",
    "morning_alarm_snoozes", "next_day_fatigue_score", "sleep_debt_category",
]


class DataLoadError(Exception):
    """Error al cargar los datos de origen."""


def load(path: Path) -> pd.DataFrame:
    """Lee el CSV y comprueba que existen todas las columnas necesarias."""
    if not path.exists():
        raise DataLoadError(f"No existe el fichero {path}")
    df = pd.read_csv(path)
    # Buscamos qué columnas necesarias no están en el CSV
    faltan = []
    for columna in COLUMNAS_REQUERIDAS:
        if columna not in df.columns:
            faltan.append(columna)

    # Si hay alguna que falta, paramos con un error claro
    if len(faltan) > 0:
        raise DataLoadError(f"Faltan columnas en el CSV: {faltan}")
    return df
