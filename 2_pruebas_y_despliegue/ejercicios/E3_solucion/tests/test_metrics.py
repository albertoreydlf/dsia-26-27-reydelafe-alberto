"""Tests de metrics.py."""

import pandas as pd

from ventas_app.metrics import top3_prod_porimporte, total_por_region


def test_total_por_region():
    validos = pd.DataFrame({
        "region": ["Norte", "Sur", "Norte"],
        "importe": [20.0, 30.0, 40.0],
    })

    totales = total_por_region(validos)

    assert totales["Norte"] == 60.0  # 20 + 40
    assert totales["Sur"] == 30.0
    assert totales.index[0] == "Norte"  # viene ordenado de mayor a menor


def test_top3_productos_por_importe():
    validos = pd.DataFrame({
        "producto": ["A", "B", "C", "D"],
        "importe": [10.0, 40.0, 30.0, 20.0],
    })

    top = top3_prod_porimporte(validos)

    assert len(top) == 3  # solo los 3 mejores
    assert list(top.index) == ["B", "C", "D"]  # de mayor a menor importe
