"""Tests de loader.py (E3 Parte 2: errores)."""

import pytest

from ventas_app.loader import DataLoadError, load


def test_load_lee_un_csv(tmp_path):
    # tmp_path es una carpeta temporal que pytest crea y borra sola
    ruta = tmp_path / "ventas.csv"
    ruta.write_text("region,unidades\nNorte,2\nSur,3\n", encoding="utf-8")

    frame = load(ruta)

    assert len(frame) == 2
    assert list(frame.columns) == ["region", "unidades"]


def test_load_con_path_inexistente_lanza_error(tmp_path):
    # Esperamos que falle con nuestra excepción de dominio
    with pytest.raises(DataLoadError):
        load(tmp_path / "no_existe.csv")
