# E3 — pytest sobre el pipeline de ventas

Solución del ejercicio E3 (sesión 28 sep). Los tests prueban el `ventas_app` de la sesión 3
(`1_programacion_avanzada_python/ventas_app/`) y el `ventas.csv` de la sesión 2.

Ejecutar desde esta carpeta:

```bash
cd 2_pruebas_y_despliegue/ejercicios/E3_solucion
pytest -q
pytest -q -m "not integration"
```

Contenido de `tests/`: `conftest.py` (fixture `ventas_mini`), `test_validator.py`, `test_loader.py`,
`test_metrics.py`, `test_cli.py` y `test_integracion.py` (CSV real: 140 válidas y 10 inválidas).
