import pandas as pd


def sueno_medio_por_uso_movil(validos: pd.DataFrame):
    """Horas de sueño medias con uso bajo (False) y alto (True) del móvil.Esto devuelve una "Series" de pandas """
    """Una Series es una lista de valores donde cada uno tiene una etiqueta (el índice). Se puede ver como una tabla de una sola columna"""
    return validos.groupby("movil_alto")["total_sleep_hours"].mean()


def fatiga_media_por_categoria(validos: pd.DataFrame):
    """Fatiga media del día siguiente según la categoría de sleep debt.Esto devuelve una "Series" de pandas"""
    return validos.groupby("sleep_debt_category")["next_day_fatigue_score"].mean().sort_values(ascending=False)


def sueno_medio_por_app(validos: pd.DataFrame):
    """Horas de sueño medias según la app que más se usa antes de dormir"""
    return validos.groupby("primary_bedtime_app")["total_sleep_hours"].mean().sort_values()


def correlacion_movil_sueno(validos: pd.DataFrame) -> float:
    """Correlación entre minutos de móvil y horas de sueño (cerca de -1: más móvil, menos sueño)"""
    return float(validos["bedtime_phone_minutes"].corr(validos["total_sleep_hours"]))
