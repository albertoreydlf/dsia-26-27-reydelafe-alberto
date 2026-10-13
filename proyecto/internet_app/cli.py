import argparse
from pathlib import Path

from internet_app.loader import load
from internet_app.validator import validar_sueno
from internet_app.metrics import (
    correlacion_movil_sueno,
    fatiga_media_por_categoria,
    sueno_medio_por_app,
    sueno_medio_por_uso_movil,
)


def parse_args():
    parser = argparse.ArgumentParser(description="Pipeline de hábitos de sueño y pantalla")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frame = load(Path(args.input))  # carga el CSV con el load de loader.py
    validos, errores = validar_sueno(frame) #usamos el codigo de validator.py
    validos.to_csv(Path(args.output), index=False)
    print(f"Hay {len(validos)} válidos y {len(errores)} inválidos")
    print("\nHoras de sueño medias según uso del móvil (True = 60 min o más):")
    print(sueno_medio_por_uso_movil(validos).round(2))
    print("\nFatiga media según categoría de deuda de sueño:")
    print(fatiga_media_por_categoria(validos).round(2))
    print("\nHoras de sueño medias según la app de antes de dormir:")
    print(sueno_medio_por_app(validos).round(2))
    print(f"\nCorrelación entre minutos de móvil y horas de sueño: {correlacion_movil_sueno(validos):.2f}")


if __name__ == "__main__":
    main()
