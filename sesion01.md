# Sesión 01 — Entornos y Git

## Entorno de desarrollo

- Python utilizado: 3.12.14.
- Se creó un entorno virtual con `venv`.
- Las dependencias del curso se instalaron desde `requirements.txt`.
- Se comprobó el entorno con `check_entorno.py --strict`.
- Resultado obtenido: `ENTORNO OK`.

## Conceptos de entornos virtuales

Un entorno virtual permite aislar las dependencias de cada proyecto.

`.venv` contiene el entorno local y no debe subirse a GitHub.

`requirements.txt` indica qué dependencias necesita el proyecto y permite reconstruir el entorno en otro ordenador.

`python -m pip` permite asegurarse de que se está utilizando el `pip` asociado al intérprete de Python activo.

## Conceptos de Git

El flujo básico de Git es:

Working tree → Staging → Commit local → Repositorio remoto

- `git status`: muestra el estado de los archivos.
- `git diff`: muestra los cambios realizados.
- `git add`: prepara los cambios para el siguiente commit.
- `git commit`: guarda una versión de los cambios en el repositorio local.
- `git push`: envía los commits locales a GitHub.
- `git pull`: trae e integra cambios desde GitHub.
- Una rama permite trabajar en cambios sin modificar directamente `main`.
- Un Pull Request propone integrar los cambios de una rama en otra.
- El merge incorpora finalmente esos cambios a la rama de destino.

## Autoevaluación

1. **¿Qué diferencia hay entre el Python global y el de `.venv`?**  
   El Python global pertenece al sistema, mientras que el de `.venv` está aislado para un proyecto concreto.

2. **¿Por qué usar `python -m pip`?**  
   Para asegurarse de que `pip` pertenece al intérprete de Python que se está utilizando.

3. **¿Qué diferencia hay entre working tree, staging y commit?**  
   Working tree contiene los cambios actuales; staging contiene los cambios seleccionados para guardar; el commit guarda esos cambios en el historial.

4. **¿Qué diferencia hay entre `git clone` y `git pull`?**  
   `git clone` crea una copia local inicial de un repositorio. `git pull` actualiza una copia local ya existente.

5. **¿Qué no debemos subir a GitHub?**  
   Entornos virtuales, archivos `.env`, claves API, secretos y archivos temporales.

6. **¿Cómo debe ser un buen mensaje de commit?**  
   Corto, claro y descriptivo del cambio realizado.

7. **¿Qué puede ocurrir si VS Code utiliza un intérprete distinto al del entorno virtual?**  
   Puede no encontrar paquetes que sí están instalados en `.venv`.

8. **¿Qué hacer si se sube accidentalmente un `.env` con secretos?**  
   Revocar inmediatamente las claves expuestas, generar nuevas claves y eliminar el secreto del repositorio.