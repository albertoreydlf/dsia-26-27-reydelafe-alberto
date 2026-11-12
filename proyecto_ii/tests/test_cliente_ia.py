"""Tests del cliente del modelo de lenguaje. Ninguno llama de verdad a NVIDIA."""

import pytest

import cliente_ia

HABITOS = {"age": 29, "bedtime_phone_minutes": 179}


class RespuestaFalsa:
    """Imita lo que devuelve la API de NVIDIA."""

    def raise_for_status(self):
        pass

    def json(self):
        return {"choices": [{"message": {"content": "Explicacion de prueba"}}]}


def test_mock_devuelve_una_explicacion():
    explicacion = cliente_ia.explicar_prediccion(HABITOS, "Moderate Debt", 0.52)

    assert isinstance(explicacion, cliente_ia.Explicacion)
    assert explicacion.proveedor == "mock"
    assert "Moderate Debt" in explicacion.texto


def test_prompt_lleva_la_prediccion_y_los_habitos():
    prompt = cliente_ia.construir_prompt(HABITOS, "Moderate Debt", 0.52)

    assert "Moderate Debt" in prompt
    assert "0.52" in prompt
    assert "bedtime_phone_minutes: 179" in prompt


def test_nvidia_sin_clave_da_error_claro(monkeypatch):
    # quitamos la clave solo durante este test
    monkeypatch.delenv("NVIDIA_API_KEY", raising=False)

    with pytest.raises(cliente_ia.ErrorClienteIA, match="NVIDIA_API_KEY"):
        cliente_ia.explicar_prediccion(HABITOS, "Moderate Debt", 0.52, proveedor="nvidia")


def test_nvidia_con_respuesta_simulada(monkeypatch):
    def post_falso(*args, **kwargs):
        return RespuestaFalsa()

    monkeypatch.setenv("NVIDIA_API_KEY", "clave-de-prueba")
    monkeypatch.setattr(cliente_ia.requests, "post", post_falso)

    explicacion = cliente_ia.explicar_prediccion(HABITOS, "Moderate Debt", 0.52, proveedor="nvidia")

    assert explicacion.proveedor == "nvidia"
    assert explicacion.texto == "Explicacion de prueba"


def test_proveedor_desconocido_da_error():
    with pytest.raises(cliente_ia.ErrorClienteIA, match="no soportado"):
        cliente_ia.explicar_prediccion(HABITOS, "Moderate Debt", 0.52, proveedor="otro")
