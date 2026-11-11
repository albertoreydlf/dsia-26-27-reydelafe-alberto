"""Cosas que comparten varios tests."""

import pandas as pd
import pytest

from ingesta import RUTA_SALIDA


@pytest.fixture
def df_muestra():
    """400 personas de la tabla real, para que los tests vayan rapido."""
    df = pd.read_csv(RUTA_SALIDA)
    return df.sample(400, random_state=0)
