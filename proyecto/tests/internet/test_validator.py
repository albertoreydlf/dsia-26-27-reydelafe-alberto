"""Tests de validator.py."""

import pandas as pd
import pytest

from internet_app.validator import validar_sueno


def test_separa_validos_e_invalidos(sueno_mini):
    validos, errores = validar_sueno(sueno_mini)
    # De las 4 filas, solo U1 es válida
    assert len(validos) == 1
    assert len(errores) == 3
    assert list(validos["user_id"]) == ["U1"]


def test_anade_la_columna_movil_alto(sueno_mini):
    validos, _ = validar_sueno(sueno_mini)
    # U1 usa el móvil 90 minutos, que son 60 o más -> movil_alto es verdadero
    assert validos["movil_alto"].iloc[0]


def test_no_modifica_el_dataframe_original(sueno_mini):
    validar_sueno(sueno_mini)
    # Trabaja sobre una copia, así que el original no gana la columna movil_alto
    assert "movil_alto" not in sueno_mini.columns


@pytest.mark.parametrize(
    ("edad", "es_valida"),
    [
        (17, False),  # menor de 18 -> inválida
        (18, True),   # justo el mínimo -> válida
        (65, True),   # justo el máximo -> válida
        (66, False),  # mayor de 65 -> inválida
    ],
)
def test_edad_en_los_bordes(sueno_mini, edad, es_valida):
    fila = sueno_mini.head(1).copy()  # la fila U1, que es válida
    fila["age"] = edad
    validos, _ = validar_sueno(fila)
    assert (len(validos) == 1) == es_valida


def test_un_valor_que_no_es_numero_es_invalido(sueno_mini):
    fila = sueno_mini.head(1).copy()
    fila["total_sleep_hours"] = "abc"  # no se puede convertir a número
    validos, errores = validar_sueno(fila)
    assert len(validos) == 0
    assert len(errores) == 1


def test_un_id_repetido_es_invalido(sueno_mini):
    fila = sueno_mini.head(1)
    repetida = pd.concat([fila, fila])  # la misma fila dos veces
    validos, errores = validar_sueno(repetida)
    # La primera se conserva y la repetida es un error
    assert len(validos) == 1
    assert len(errores) == 1


def test_los_porcentajes_de_sueno_no_pasan_de_100(sueno_mini):
    fila = sueno_mini.head(1).copy()
    fila["deep_sleep_pct"] = 70.0
    fila["rem_sleep_pct"] = 50.0  # 70 + 50 = 120 -> inválida
    validos, _ = validar_sueno(fila)
    assert len(validos) == 0
