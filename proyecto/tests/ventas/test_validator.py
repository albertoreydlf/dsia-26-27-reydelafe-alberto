"""Tests de validator.py (E3 Partes 1 y 2)."""

import pandas as pd
import pytest

from ventas_app.validator import validar_ventas


def test_separa_validos_e_invalidos(ventas_mini):
    # Act: llamamos a la función con los datos de la fixture
    validos, errores = validar_ventas(ventas_mini)
    # Assert: de las 3 filas, 1 es válida y 2 son inválidas
    assert len(validos) == 1
    assert len(errores) == 2


def test_calcula_el_importe(ventas_mini):
    validos, _ = validar_ventas(ventas_mini)
    # La fila válida tiene 2 unidades a 10.0 euros -> 20.0
    assert validos["importe"].iloc[0] == 20.0


def test_no_modifica_el_dataframe_original(ventas_mini):
    validar_ventas(ventas_mini)
    # La función trabaja sobre una copia, así que el original no gana la columna importe
    assert "importe" not in ventas_mini.columns


@pytest.mark.parametrize(
    ("precio", "es_valido"),
    [
        (0, False),   # precio cero -> inválido
        (-1, False),  # precio negativo -> inválido
        (1, True),    # precio positivo -> válido
    ],
)
def test_precios_en_los_bordes(precio, es_valido):
    # Una sola fila: lo único que cambia entre casos es el precio
    frame = pd.DataFrame({"unidades": [3], "precio_unitario": [precio]})
    validos, _ = validar_ventas(frame)
    assert (len(validos) == 1) == es_valido
