# Uso de IA

## Asistente usado para desarrollar

- **Asistente:** Claude (Anthropic).
- **Qué aportó:** propuso la estructura del proyecto y escribió la mayor parte del código y de los tests, paso a paso. También me explicó cada parte de forma detallada para poder entender qué hace cada parte del código.
- **Qué hice yo:**
  - **Planteamiento:** elegí el tema y el dataset, hablé con el profesor para ver cómo enriquecerlo con una API de clima y él me confirmó que se podía asignar la ciudad y la fecha de forma sintética. Elegí las cinco ciudades.
  - **Dirección del trabajo:** fui paso a paso, sin avanzar al siguiente hasta entender el anterior. 
  - **Decisiones de machine learning:** planteé dividir los datos en train, validación y test, y pedí cambiar el código al estilo de clase (X e y), que es el que conozco. Cuestioné el uso de one-hot en todas las columnas de texto (nominales frente a ordinales)
  - **Ejecución y comprobación:** lancé yo todo en mi ordenador y revisé las salidas: la descarga real del clima, el entrenamiento, el pipeline completo, la llamada real al modelo de lenguaje y los 17 tests. Antes de programar la ingesta probé la URL de la API en el navegador.
  - **APIs y claves:** creé las cuentas y las claves. Con Hugging Face llegué hasta el error 402, comprobé en la página de facturación que la cuenta no tenía crédito y pregunté al profesor por una alternativa. Con su recomendación, saqué de la web de NVIDIA el modelo y el ejemplo de código para adaptar el cliente.
  - **Documentación:** revisé y corregí todos los documentos
- **Comandos de evidencia:**
  - `python proyecto_ii/pipeline.py --sin-descarga --proveedor nvidia`
  - `cd proyecto_ii && pytest -v` (17 passed)

## Modelo de lenguaje usado dentro del proyecto

- **Proveedor:** NVIDIA (https://build.nvidia.com).
- **Tarea:** chat (generación de texto).
- **Modelo:** `nvidia/nemotron-3.5-super-vl-120b-a12b`.
- **Para qué:** explicar con palabras la predicción del modelo de scikit-learn.
- **Qué acepté:** la respuesta se muestra tal cual en los logs del pipeline. No se usa para tomar ninguna decisión ni cambia la predicción.
- **En los tests:** siempre se usa el modo `mock`, sin internet ni clave.

## Hugging Face

Fue la primera opción. El token funcionaba, pero la API devolvió un error 402 (Payment Required). Por recomendación del profesor se usa NVIDIA. El código de Hugging Face queda comentado en `cliente_ia.py`.
