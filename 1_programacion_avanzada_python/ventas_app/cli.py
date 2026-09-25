import argparse
from pathlib import Path

from ventas_app.loader import load
from ventas_app.validator import validar_ventas
from ventas_app.metrics import total_por_region

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    frame = load(Path(args.input))  #llamamos a la funcionn que cree en loader(carga el csv)
    validos, errores = validar_ventas(frame) 
    totales = total_por_region(validos)
    validos.to_csv(Path(args.output), index=False)
    print(f"Hay {len(validos)} válidos y {len(errores)} invalidos")
    print(totales)


if __name__ == "__main__":
    main()