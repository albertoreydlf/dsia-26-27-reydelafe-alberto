"""Tests de cli.py (smoke test: comprobamos que el programa corre de principio a fin)."""

import sys

import pandas as pd

from internet_app.cli import main


def test_main_genera_el_csv_de_salida(tmp_path, monkeypatch, capsys, sueno_mini):
    entrada = tmp_path / "entrada.csv"
    salida = tmp_path / "salida.csv"
    sueno_mini.to_csv(entrada, index=False)

    # Simulamos que el usuario escribe: --input ... --output ...
    monkeypatch.setattr(sys, "argv", ["cli", "--input", str(entrada), "--output", str(salida)])

    main()

    # Se ha creado el CSV de salida y solo contiene la fila válida
    assert salida.exists()
    assert len(pd.read_csv(salida)) == 1
    # Y por pantalla se imprime el resumen
    assert "Hay 1 válidos y 3 inválidos" in capsys.readouterr().out
