# Proyecto II - Sueño, hábitos nocturnos y clima

Este proyecto predice la categoría de deuda de sueño de una persona a partir de sus hábitos antes de dormir (minutos de móvil, cafeína, ejercicio...) y del clima de ese día. Después, un modelo de lenguaje explica la predicción con palabras sencillas.

Todo se ejecuta con un solo comando y es la base del Proyecto III.

## Qué hace, paso a paso

```text
CSV del sueño + API del clima  ->  ingesta.py        (une las dos fuentes en una tabla)
tabla unida                    ->  entrenamiento.py  (entrena y guarda el modelo de scikit-learn)
modelo guardado                ->  procesamiento.py  (carga el modelo y predice)
predicción                     ->  cliente_ia.py     (un modelo de lenguaje la explica)
```

`pipeline.py` lanza los cuatro pasos en orden y va escribiendo logs de lo que hace.

## Datos

### Dataset del sueño

- Nombre: Sleep Debt and Screen Time: Late Night Phone Habits
- Origen: https://www.kaggle.com/datasets/samartalwar/sleep-debt-and-screen-time-late-night-phone-habits
- Autor: samartalwar (Kaggle)
- Licencia: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
- Fecha de descarga: 11 de octubre de 2026
- Tiene 8.500 filas y 18 columnas, sin huecos. No he modificado el fichero original.

### Clima

- Fuente: API histórica de Open-Meteo (https://open-meteo.com/). Es gratuita y no pide clave.
- Se descarga el clima diario de 2025 de cinco ciudades: Madrid, Barcelona, Sevilla, Las Palmas de Gran Canaria y Santa Cruz de Tenerife.
- Variables: temperatura media, máxima y mínima, lluvia, horas de luz, humedad, presión, nubosidad y viento máximo.

### Aviso importante: la ciudad y la fecha son inventadas

El dataset del sueño no dice dónde vive cada persona ni qué día se midió. Para poder unir el clima, a cada persona se le asigna una ciudad y una fecha al azar (con semilla fija, para que salga siempre igual). Aunque no tenga mucha utilidad real se hace porque es un trabajo de clase,uniendo a nuestros datos datos externos

El clima es real, pero la unión es sintética. Por eso **no se puede sacar ninguna conclusión sobre si el clima afecta al sueño**.Es todo una prueba.


### Por qué estos datos

Me interesa la relación entre lo que hacemos antes de dormir y cómo descansamos. Ya trabajé con este dataset en el Proyecto I, así que lo conocía y sabía que estaba limpio.

## Estructura

```text
proyecto_ii/
  ingesta.py         (lee el CSV, descarga el clima y une las dos tablas)
  entrenamiento.py   (entrena el modelo, lo mide y lo guarda)
  procesamiento.py   (carga el modelo y predice)
  cliente_ia.py      (explica la predicción: modo mock y API de NVIDIA)
  pipeline.py        (ejecuta todo en orden)
  tests/             (17 tests con pytest)
  data/              (el CSV original y la tabla con clima)
  models/            (el modelo entrenado y sus métricas)
  .env.example       (plantilla de las claves, sin valores)
  requirements.txt
  AI_USAGE.md
```

## Instalación

Desde la raíz del repositorio, con el entorno virtual activado:

```bash
pip install -r proyecto_ii/requirements.txt
```

Para usar el modelo de lenguaje real hace falta una clave gratuita de NVIDIA (https://build.nvidia.com).(Iniciar sesiony pedir una PAI_KEY,que es gratis,a diferencia de la de hugging face) Se copia la plantilla y se rellena:

```bash
cp proyecto_ii/.env.example proyecto_ii/.env
```

El fichero `.env` no se sube a Git. Sin la clave de nvidia, el proyecto funciona igual en modo `mock`,aunque este es un mensaje predeterminado que he creado 
y que responde siempre igual

## Cómo ejecutarlo

```bash
python proyecto_ii/pipeline.py                                    # todo, con la explicación en modo mock
python proyecto_ii/pipeline.py --proveedor nvidia                 # todo, con la explicación del modelo de la API de NVIDIA
python proyecto_ii/pipeline.py --sin-descarga                     # sin volver a pedir el clima (usa la tabla guardada)
python proyecto_ii/pipeline.py --sin-descarga --proveedor nvidia  # lo mismo, con el modelo de lenguaje real
```

- `--sin-descarga` no vuelve a llamar a la API del clima: usa la tabla con clima que ya está guardada en `data/`. El resultado es el mismo, porque la descarga da siempre la misma tabla.
- `--proveedor` elige quién explica la predicción: `mock` (por defecto) o `nvidia`.

Cada fichero también se puede lanzar por separado, por ejemplo `python proyecto_ii/entrenamiento.py`.

## Modelo de scikit-learn

- **Qué predice:** la columna `sleep_debt_category`, que tiene cuatro valores: Optimal Recovery, Mild Deficit, Moderate Debt y Severe Sleep Debt.
- **Con qué:** 10 hábitos de antes de dormir (edad, género, ocupación, cronotipo, minutos de móvil, app principal, brillo de pantalla, filtro de luz azul, cafeína y ejercicio) y las 9 variables de clima (temperatura media, máxima y mínima, lluvia, horas de luz, humedad, presión, nubosidad y viento máximo).
- **Qué se deja fuera:** las horas dormidas y el resto de medidas de después de dormir. La categoría se calcula a partir de las horas dormidas, así que usarlas sería hacer trampa: el modelo acertaría casi el 100 % sin aprender nada (fuga de información).
- **Modelo:** un Random Forest dentro de un `Pipeline` de scikit-learn, que también convierte las columnas de texto en números (one-hot).
- **Reparto de datos:** 70 % train, 15 % validación y 15 % test (5.950, 1.275 y 1.275 personas), manteniendo la proporción de las categorías.
- **Dónde se guarda:** `models/modelo.joblib`. Las métricas quedan en `models/metricas.json`.
- **Versión:** el modelo guardado se entrenó con scikit-learn 1.9.1. Con otra versión puede salir un aviso al cargarlo; en ese caso basta con volver a entrenarlo con `python proyecto_ii/entrenamiento.py`, que tarda un segundo. Los números pueden cambiar un poco de una versión a otra.

### Resultados

Se entrenan dos modelos con las mismas personas, uno sin clima y otro con clima, y se comparan en validación:

| Medida (validación) | Sin clima | Con clima |
| --- | --- | --- |
| Accuracy | 72,3 % | 71,5 % |
| F1 macro | 0,642 | 0,615 |

El modelo que se guarda es el que usa clima. En test saca:

| Medida (test) | Valor |
| --- | --- |
| Accuracy | 68,4 % |
| F1 macro | 0,572 |
| Acierto diciendo siempre la categoría más común | 52,5 % |

Cómo lo leo:

- Los hábitos sí ayudan a predecir: el modelo acierta unos 16 puntos más que decir siempre la categoría más común.
- **El clima no mejora la predicción**, sale incluso un poco peor. Es lo esperado, porque la ciudad y la fecha son inventadas y el clima no tiene relación real con cada persona.
- Se guarda el modelo con clima de todas formas, porque es el recorrido completo (datos + API + modelo) que se ampliará en el Proyecto III.
- El modelo falla sobre todo con los casos graves (Severe Sleep Debt), que confunde con Moderate Debt. Por eso el F1 macro es más bajo que el accuracy.

## Modelo de lenguaje por API

- **Proveedor:** NVIDIA (https://build.nvidia.com), con una cuenta gratuita de desarrollador.
- **Tarea:** chat (generación de texto).
- **Modelo:** `nvidia/nemotron-3.5-super-vl-120b-a12b`.
- **Para qué se usa:** recibe la predicción del modelo de scikit-learn, su confianza y los hábitos de la persona, y devuelve una explicación de tres frases en español con un consejo.
- **Modo mock:** devuelve un texto fijo sin usar internet ni clave. Es el modo por defecto y el único que usan los tests.

Ejemplo de respuesta real:

> El modelo predice que tienes una "Deuda de Sueño Moderada", lo que significa que probablemente no estás descansando lo suficiente. La confianza de la predicción es de 0.52, por lo que es un resultado con certeza baja y solo una referencia. Intenta reducir el uso del teléfono antes de dormir, especialmente Instagram y Reddit, para mejorar la calidad de tu descanso.

### Por qué NVIDIA y no Hugging Face

El enunciado recomienda Hugging Face y fue lo primero que probé porque es lo que se dijo en clase. Creé la cuenta y un token con permiso de inferencia, y el token funcionaba, pero la API devolvió un error 402 (Payment Required),porque no tenia creditos,que son de pago. Despues de escribir un correo a david,me recomendo esta api de nvidia y la use,que si que es gratis y ademas proporciona un modelo de lenguaje bueno, que da respuesta completas.Le desactive el modo de "pensar" porque como tiene que responder solo con tres frases no es necesario

El código de Hugging Face sigue en `cliente_ia.py`, comentado y con una nota que explica esto. `.env.example` mantiene también `HF_TOKEN=` por si en el futuro tengo créditos y los quiero usar.

## Tests

```bash
cd proyecto_ii
pytest -v
```

Hay 17 tests: 16 unitarios y 1 de integración. Ninguno usa internet: la API del clima y la de NVIDIA se sustituyen por imitaciones. Uno de ellos carga el modelo guardado y comprueba que predice.

## Qué se ampliará en el Proyecto III

- Una API propia para pedir predicciones (usará `predecir` de `procesamiento.py` y `explicar_prediccion` de `cliente_ia.py`).
- Integración continua (CI) con estos tests.
- Más robustez, despliegue y monitorización.

El código está separado en un fichero por tarea para poder añadir todo eso sin reescribir lo que ya hay.

## Uso de IA

Está explicado en `AI_USAGE.md`.
