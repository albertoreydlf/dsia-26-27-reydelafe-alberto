"""Tests de metrics.py."""

import pandas as pd
import pytest

from internet_app.metrics import (
    correlacion_movil_sueno,
    fatiga_media_por_categoria,
    sueno_medio_por_app,
    sueno_medio_por_uso_movil,
)


@pytest.fixture
def validos_mini():
    """Seis personas ya validadas, con números fáciles para calcular a mano."""
    return pd.DataFrame({
        "bedtime_phone_minutes": [20, 30, 90, 120, 45, 150],
        "movil_alto": [False, False, True, True, False, True],
        "total_sleep_hours": [8.0, 7.0, 5.0, 4.0, 7.5, 3.5],
        "next_day_fatigue_score": [1.0, 2.0, 7.0, 9.0, 2.0, 10.0],
        "sleep_debt_category": [
            "Optimal Recovery", "Mild Deficit", "Moderate Debt",
            "Severe Sleep Debt", "Mild Deficit", "Severe Sleep Debt",
        ],
        "primary_bedtime_app": [
            "News / Reading", "YouTube", "TikTok / Reels",
            "TikTok / Reels", "YouTube", "TikTok / Reels",
        ],
    })


def test_sueno_medio_por_uso_movil(validos_mini):
    resultado = sueno_medio_por_uso_movil(validos_mini)

    assert resultado[False] == 7.5                           # (8 + 7 + 7.5) / 3
    assert resultado[True] == pytest.approx(4.17, abs=0.01)  # (5 + 4 + 3.5) / 3 = 4.1666...


def test_fatiga_media_por_categoria(validos_mini):
    resultado = fatiga_media_por_categoria(validos_mini)

    assert resultado["Severe Sleep Debt"] == 9.5       # (9 + 10) / 2
    assert resultado["Mild Deficit"] == 2.0            # (2 + 2) / 2
    assert resultado.index[0] == "Severe Sleep Debt"   # va primero la de más fatiga


def test_sueno_medio_por_app(validos_mini):
    resultado = sueno_medio_por_app(validos_mini)

    assert resultado["YouTube"] == 7.25                # (7 + 7.5) / 2
    assert resultado.index[0] == "TikTok / Reels"      # va primera la app con menos sueño


def test_correlacion_movil_sueno_es_negativa(validos_mini):
    resultado = correlacion_movil_sueno(validos_mini)

    # Más minutos de móvil, menos horas de sueño: la correlación es casi -1
    assert resultado == pytest.approx(-0.98, abs=0.01)
