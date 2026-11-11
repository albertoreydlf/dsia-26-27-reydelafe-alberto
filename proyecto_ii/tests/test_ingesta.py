"""Tests de la ingesta. Ninguno llama de verdad a la API del clima."""

import pandas as pd
import pytest
import requests

import ingesta


class RespuestaFalsa:
    """Imita lo que devuelve la API del clima, con solo dos dias."""

    def raise_for_status(self):
        pass

    def json(self):
        return {"daily": {"time": ["2025-01-01", "2025-01-02"], "temperature_2m_mean": [10.0, 12.0]}}


def test_sorteo_sale_siempre_igual():
    df = pd.DataFrame({"user_id": range(50)})
    primera_vez = ingesta.asignar_ciudad_y_fecha(df)
    segunda_vez = ingesta.asignar_ciudad_y_fecha(df)
    assert primera_vez.equals(segunda_vez)


def test_sorteo_usa_ciudades_y_fechas_validas():
    df = ingesta.asignar_ciudad_y_fecha(pd.DataFrame({"user_id": range(50)}))
    assert set(df["ciudad"]) <= set(ingesta.CIUDADES)
    assert df["fecha"].between(ingesta.FECHA_INICIO, ingesta.FECHA_FIN).all()


def test_descargar_clima_sin_internet(monkeypatch):
    def get_falso(*args, **kwargs):
        return RespuestaFalsa()

    # cambiamos requests.get por la imitacion solo durante este test
    monkeypatch.setattr(ingesta.requests, "get", get_falso)

    clima = ingesta.descargar_clima_ciudad("Madrid", 40.4, -3.7)

    assert list(clima["fecha"]) == ["2025-01-01", "2025-01-02"]
    assert list(clima["ciudad"]) == ["Madrid", "Madrid"]


def test_error_claro_si_falla_la_api(monkeypatch):
    def get_roto(*args, **kwargs):
        raise requests.ConnectionError("sin red")

    monkeypatch.setattr(ingesta.requests, "get", get_roto)

    # comprobamos que salta nuestro error y que dice de que ciudad era
    with pytest.raises(RuntimeError, match="Madrid"):
        ingesta.descargar_clima_ciudad("Madrid", 40.4, -3.7)


def test_unir_no_pierde_personas():
    personas = pd.DataFrame({
        "user_id": ["A", "B"],
        "ciudad": ["Madrid", "Sevilla"],
        "fecha": ["2025-01-01", "2025-01-02"],
    })
    clima = pd.DataFrame({
        "ciudad": ["Madrid", "Sevilla"],
        "fecha": ["2025-01-01", "2025-01-02"],
        "temperature_2m_mean": [10.0, 15.0],
    })

    unido = ingesta.unir(personas, clima)

    assert len(unido) == 2
    assert list(unido["temperature_2m_mean"]) == [10.0, 15.0]
