"""Tests del entrenamiento, con una muestra pequena para que vayan rapido."""

import entrenamiento


def test_reparto_70_15_15(df_muestra):
    X_train, X_val, X_test, y_train, y_val, y_test = entrenamiento.dividir_datos(df_muestra)

    # de 400 personas: 280 train, 60 validacion y 60 test
    assert len(X_train) == 280
    assert len(X_val) == 60
    assert len(X_test) == 60
    assert len(y_train) == 280


def test_las_entradas_no_llevan_la_respuesta(df_muestra):
    X_train, X_val, X_test, y_train, y_val, y_test = entrenamiento.dividir_datos(df_muestra)

    # si alguna de estas estuviera en X el modelo haria trampa
    assert entrenamiento.OBJETIVO not in X_train.columns
    assert "total_sleep_hours" not in X_train.columns


def test_entrenar_y_evaluar(df_muestra):
    X_train, X_val, X_test, y_train, y_val, y_test = entrenamiento.dividir_datos(df_muestra)

    modelo = entrenamiento.entrenar(X_train, y_train)
    metricas = entrenamiento.evaluar(modelo, X_val, y_val)

    assert set(metricas) == {"accuracy", "f1_macro"}
    assert 0 <= metricas["accuracy"] <= 1
    assert 0 <= metricas["f1_macro"] <= 1
