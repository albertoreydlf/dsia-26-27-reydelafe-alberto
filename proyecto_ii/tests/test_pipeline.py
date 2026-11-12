"""Test de integracion: prueba que todas las piezas encajan una detras de otra."""

import joblib
import pytest

import entrenamiento
import pipeline
import procesamiento


@pytest.mark.integration
def test_recorrido_completo_con_mock(df_muestra, tmp_path):
    # 1. entrenar un modelo con la muestra
    X_train, X_val, X_test, y_train, y_val, y_test = entrenamiento.dividir_datos(df_muestra)
    modelo = entrenamiento.entrenar(X_train, y_train)

    # 2. guardarlo y volver a cargarlo (en una carpeta temporal, no en models/)
    ruta_modelo = tmp_path / "modelo.joblib"
    joblib.dump(modelo, ruta_modelo)
    modelo_cargado = procesamiento.cargar_modelo(ruta_modelo)

    # 3. predecir con el modelo cargado
    resultado = procesamiento.predecir(modelo_cargado, df_muestra)
    assert len(resultado) == len(df_muestra)

    # 4. explicar la prediccion de una persona con el mock
    explicacion = pipeline.explicar_ejemplo(resultado, proveedor="mock")
    assert explicacion.proveedor == "mock"
    assert resultado.iloc[0]["prediccion"] in explicacion.texto
