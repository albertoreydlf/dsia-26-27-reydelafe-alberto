# Diseño de ventas_app

Principios SOLID aplicados a mi codigo

S — Single Responsibility (responsabilidad única) : lo vemos en validator.py Este fichero solo valida, no hace nada más. No carga el CSV ni calcula totales, únicamente decide qué filas son válidas y cuáles no. Así, si el día de mañana cambian las reglas de validación, solo tengo que tocar este fichero, sin arriesgarme a romper la carga de datos o los cálculos.

S — Single Responsibility (responsabilidad única) : lo vemos tambien en cli.py.Su función main() únicamente llama en orden a load, validar_ventas y total_por_region. Esto hace que si algún día cambio cómo se valida o cómo se calcula, cli.py no se entera de nada, solo sigue llamando a las mismas funciones.

O — Open/Closed (abierto a extensión, cerrado a modificación), lo vemos en metrics.py.Este fichero se puede ampliar sin tocar lo que ya funciona. Ahora mismo tiene total_por_region y top3_prod_porimporte. Si quisiera añadir una nueva métrica (por ejemplo, total_por_producto), añadiría una función nueva en este mismo fichero, sin modificar ni arriesgar las que ya están hechas y probadas.

