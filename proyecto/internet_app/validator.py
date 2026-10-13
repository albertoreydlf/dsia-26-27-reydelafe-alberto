import pandas as pd

CATEGORIAS_VALIDAS = ["Optimal Recovery", "Mild Deficit", "Moderate Debt", "Severe Sleep Debt"]
UMBRAL_MOVIL_ALTO = 60  # minutos de móvil antes de dormir a partir de los cuales el uso es "alto"

# Columnas que deben ser números
COLUMNAS_NUMERICAS = [
    "age", "bedtime_phone_minutes", "screen_brightness_pct", "blue_light_filter_active",
    "total_sleep_hours", "deep_sleep_pct", "rem_sleep_pct", "next_day_fatigue_score",
]


def validar_sueno(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    copia = frame.copy()  # trabajamos sobre una copia para no modificar el original
    # Si un valor no se puede convertir a número, pasa a NaN (y la fila será inválida)
    for col in COLUMNAS_NUMERICAS:
        copia[col] = pd.to_numeric(copia[col], errors="coerce")

    # Reglas: una fila es válida solo si cumple TODAS (los NaN no cumplen ninguna)
    ok = (
        copia["user_id"].notna()
        & ~copia["user_id"].duplicated()                       # sin ids repetidos
        & copia["age"].between(18, 65)                         # edad entre 18 y 65
        & copia["bedtime_phone_minutes"].between(0, 180)       # minutos de móvil entre 0 y 180
        & copia["screen_brightness_pct"].between(0, 100)       # brillo es un porcentaje
        & copia["blue_light_filter_active"].isin([0, 1])       # filtro: 0 (no) o 1 (sí)
        & copia["total_sleep_hours"].between(1, 24)            # horas de sueño razonables
        & ((copia["deep_sleep_pct"] + copia["rem_sleep_pct"]) <= 100)  # los % no pueden pasar de 100
        & copia["next_day_fatigue_score"].between(1, 10)       # fatiga de 1 a 10
        & copia["sleep_debt_category"].isin(CATEGORIAS_VALIDAS)  # categoría conocida
    )

    validos = copia.loc[ok].copy()   # filas que cumplen todas las reglas
    errores = copia.loc[~ok].copy()  # ~ok son las que NO las cumplen
    validos["movil_alto"] = validos["bedtime_phone_minutes"] >= UMBRAL_MOVIL_ALTO
    return validos, errores
