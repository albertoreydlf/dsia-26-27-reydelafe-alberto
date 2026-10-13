"""Tests de loader.py."""

import pytest

from internet_app.loader import DataLoadError, load


def test_load_lee_un_csv(tmp_path, sueno_mini):
    # tmp_path es una carpeta temporal que pytest crea y borra sola
    ruta = tmp_path / "sueno.csv"
    sueno_mini.to_csv(ruta, index=False)

    frame = load(ruta)

    assert len(frame) == 4


def test_load_con_path_inexistente_lanza_error(tmp_path):
    with pytest.raises(DataLoadError):
        load(tmp_path / "no_existe.csv")


def test_load_con_columnas_que_faltan_lanza_error(tmp_path, sueno_mini):
    ruta = tmp_path / "incompleto.csv"
    sueno_mini.drop(columns=["age"]).to_csv(ruta, index=False)  # quitamos la columna age

    # match comprueba que el mensaje de error menciona la columna que falta
    with pytest.raises(DataLoadError, match="age"):
        load(ruta)
