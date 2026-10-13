"""Test de integración con el CSV real del curso (E3 Parte 3)."""

from pathlib import Path

import pytest

from ventas_app.loader import load
from ventas_app.validator import validar_ventas

# CSV del curso (sesión 2): parents[4] sube hasta la raíz del repo
CSV_CURSO = Path(__file__).resolve().parents[4] / "1_programacion_avanzada_python" / "Datos" / "ventas.csv"


@pytest.mark.integration
def test_csv_curso_tiene_140_validas_y_10_invalidas():
    frame = load(CSV_CURSO)

    validos, errores = validar_ventas(frame)

    assert len(validos) == 140
    assert len(errores) == 10
