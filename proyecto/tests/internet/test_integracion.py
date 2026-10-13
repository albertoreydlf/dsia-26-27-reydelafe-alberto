"""Test de integración con el CSV real del dataset de Kaggle."""

from pathlib import Path

import pytest

from internet_app.loader import load
from internet_app.validator import validar_sueno

# proyecto/data/bedtime_screentime_sleep_debt.csv, calculado desde la ubicación de este fichero
CSV_SUENO = Path(__file__).resolve().parents[2] / "data" / "bedtime_screentime_sleep_debt.csv"


@pytest.mark.integration
def test_csv_real_tiene_8500_validas_y_ninguna_invalida():
    frame = load(CSV_SUENO)

    validos, errores = validar_sueno(frame)

    assert len(validos) == 8500
    assert len(errores) == 0
