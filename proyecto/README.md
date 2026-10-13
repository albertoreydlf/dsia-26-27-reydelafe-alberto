# Proyecto I - Programación avanzada en Python

En este proyecto hay dos programas que hacen lo mismo con datos distintos: cargan un CSV, comprueban qué filas son correctas, calculan unas métricas y se pueden ejecutar desde la terminal. Los dos tienen tests con pytest y un CI en GitHub Actions.

- Parte A: `ventas_app`, con el dataset de ventas del curso.
- Parte B: `internet_app`, con un dataset de Kaggle sobre sueño y uso del móvil.

## Estructura

```text
proyecto/
  ventas_app/       (Parte A: loader.py, validator.py, metrics.py, cli.py)
  internet_app/     (Parte B: loader.py, validator.py, metrics.py, cli.py)
  tests/ventas/     (tests de la Parte A)
  tests/internet/   (tests de la Parte B)
  data/             (los dos CSV)
  pytest.ini
```

El fichero del CI está en la raíz del repositorio: `.github/workflows/ci.yml`.

## Instalación

Desde la raíz del repositorio, con el entorno virtual activado:

```bash
pip install -r requirements.txt
```

## Parte A: ventas_app

Carga `ventas.csv`, separa las filas válidas de las inválidas (las unidades y el precio tienen que existir y ser mayores que 0), calcula el importe de cada venta y enseña el total por región.

```bash
cd proyecto
python -m ventas_app.cli --input data/ventas.csv --output /tmp/ventas_limpias.csv
```

Con el CSV del curso salen 140 filas válidas y 10 inválidas.

## Parte B: internet_app

### Dataset

- Nombre: Sleep Debt and Screen Time: Late Night Phone Habits
- Origen: https://www.kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits
- Autor: samartalwar (Kaggle)
- Licencia: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
- Fecha de descarga: 11 de octubre de 2026
- No he modificado el fichero. Tiene 8.500 filas y 18 columnas.

### Qué hace

Carga el CSV, comprueba cada fila con las reglas de abajo, guarda las filas válidas en un CSV nuevo y enseña cuatro métricas por pantalla.

```bash
cd proyecto
python -m internet_app.cli --input data/bedtime_screentime_sleep_debt.csv --output /tmp/sueno_validos.csv
```

### Reglas de validación

Una fila es válida solo si cumple todas estas reglas:

- El `user_id` existe y no está repetido.
- La edad está entre 18 y 65.
- Los minutos de móvil antes de dormir están entre 0 y 180.
- El brillo de la pantalla está entre 0 y 100.
- El filtro de luz azul es 0 o 1.
- Las horas de sueño están entre 1 y 24.
- El sueño profundo más el REM no pasan de 100 %.
- La fatiga del día siguiente está entre 1 y 10.
- La categoría de deuda de sueño es una de las cuatro que existen.

Si un valor no es un número o está vacío, la fila cuenta como inválida. Con el dataset real todas las filas son válidas. A las filas válidas les añado una columna `movil_alto`, que es verdadera si usan el móvil 60 minutos o más antes de dormir.

### Métricas

1. Horas de sueño medias con uso bajo y uso alto del móvil.
2. Fatiga media según la categoría de deuda de sueño.
3. Horas de sueño medias según la app que más se usa antes de dormir.
4. Correlación entre los minutos de móvil y las horas de sueño.

## Tests

Desde la carpeta `proyecto/`:

```bash
pytest -q
pytest -q -m "not integration"
pytest --cov=ventas_app --cov=internet_app --cov-report=term-missing --cov-fail-under=60
```

El primer comando ejecuta los 31 tests (12 de la Parte A y 19 de la Parte B). El segundo se salta los 2 tests de integración, que usan los CSV reales. El tercero mide la cobertura y falla si baja del 60 %. Ahora está en el 98 %.

## CI

El workflow está en `.github/workflows/ci.yml`. Se ejecuta en cada push a `main` o a una rama `practica/`, y en cada pull request. Instala las dependencias, pasa los tests del ejercicio E3 y los de este proyecto con el mínimo de cobertura del 60 %.

Ejecuciones: https://github.com/albertoreydlf/dsia-26-27-reydelafe-alberto/actions/workflows/ci.yml

## Uso de IA

Para hacer este proyecto he usado Claude como ayuda.