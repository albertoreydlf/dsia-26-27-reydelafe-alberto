import pandas as pd


class ValidationError(Exception):
    """Datos que no cumplen reglas de negocio."""
    

def validar_ventas(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    copia_datos = frame.copy() #lo usamos para trabajar sobre una copia
    copia_datos["unidades"] = pd.to_numeric(copia_datos["unidades"], errors = "coerce")
    copia_datos["precio_unitario"] = pd.to_numeric(copia_datos["precio_unitario"], errors = "coerce")
    
    # regla: unidades y precio existen y son mayores que 0
    ok = (
        copia_datos["unidades"].notna()
        & (copia_datos["unidades"] > 0)
        & copia_datos["precio_unitario"].notna()
        & (copia_datos["precio_unitario"] > 0)
    )

    validos = copia_datos.loc[ok].copy()        #cuando se cumpla ok
    errores = copia_datos.loc[~ok].copy()       #~ok es cuando NO se cumpla ok
    validos["importe"] = validos["unidades"] * validos["precio_unitario"]
    return validos, errores