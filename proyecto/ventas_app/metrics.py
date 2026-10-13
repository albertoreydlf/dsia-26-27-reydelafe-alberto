import pandas as pd


def total_por_region(validos: pd.DataFrame):
    return validos.groupby("region")["importe"].sum().sort_values(ascending=False)

TOP_N = 3 #numero de productos que queremos mostrar
def top3_prod_porimporte(validos: pd.DataFrame):
    return validos.groupby("producto")["importe"].sum().sort_values(ascending=False).head(TOP_N)