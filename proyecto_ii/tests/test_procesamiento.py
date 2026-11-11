"""Tests de la inferencia. Usan el modelo de verdad que esta en models/."""

import pytest

import procesamiento


def test_modelo_guardado_carga_y_predice(df_muestra):
    modelo = procesamiento.cargar_modelo()

    resultado = procesamiento.predecir(modelo, df_muestra)

    assert len(resultado) == len(df_muestra)
    # todas las predicciones tienen que ser una de las 4 categorias del modelo
    assert set(resultado["prediccion"]) <= set(modelo.classes_)
    assert resultado["confianza"].between(0, 1).all()


def test_error_si_no_existe_el_modelo(tmp_path):
    with pytest.raises(FileNotFoundError):
        procesamiento.cargar_modelo(tmp_path / "no_existe.joblib")


def test_error_si_faltan_columnas(df_muestra):
    modelo = procesamiento.cargar_modelo()

    with pytest.raises(ValueError, match="Faltan columnas"):
        procesamiento.predecir(modelo, df_muestra[["age"]])
