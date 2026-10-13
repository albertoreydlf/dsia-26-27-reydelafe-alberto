"""Fixtures compartidas por los tests de ventas_app."""

import pandas as pd
import pytest


@pytest.fixture
def ventas_mini():
    """DataFrame pequeño en memoria: 1 fila válida y 2 inválidas."""
    return pd.DataFrame({
        "fecha": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "region": ["Norte", "Sur", "Norte"],
        "producto": ["A", "B", "A"],
        "unidades": [2, None, 5],             # la fila 2 no tiene unidades -> inválida
        "precio_unitario": [10.0, 20.0, -1.0],  # la fila 3 tiene precio negativo -> inválida
        "cliente_id": ["C1", "C2", "C1"],
    })
