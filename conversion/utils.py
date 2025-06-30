import requests
from datetime import datetime
from decimal import Decimal

USER = "gustavogongoraortiz@gmail.com"
PASS = "@Eldiablo1"
SERIE = "F073.TCO.PRE.Z.D"

def obtener_valor_dolar():
    """
    Consulta el valor del dólar observado desde la API REST del Banco Central de Chile.
    """
    fecha = datetime.now().strftime("%Y-%m-%d")

    url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
    params = {
        "user": USER,
        "pass": PASS,
        "function": "GetSeries",
        "timeseries": SERIE,
        "firstdate": fecha,
        "lastdate": fecha
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data["Codigo"] == 0 and data["Series"]["Obs"]:
            return float(data["Series"]["Obs"][0]["value"])
        else:
            return None
    except Exception as e:
        print(f"Error al consultar el dólar: {e}")
        return None

def convertir_monto(monto, moneda_origen, moneda_destino):
    """
    Convierte un monto de una moneda a otra.
    
    Args:
        monto: Cantidad a convertir (Decimal)
        moneda_origen: Moneda de origen ('CLP', 'USD', etc.)
        moneda_destino: Moneda de destino ('CLP', 'USD', etc.)
    
    Returns:
        Decimal: Monto convertido
    """
    if moneda_origen == moneda_destino:
        return monto
    
    # Para pruebas, usamos un valor fijo del dólar
    if moneda_origen == 'CLP' and moneda_destino == 'USD':
        # Valor aproximado del dólar para pruebas
        valor_dolar = obtener_valor_dolar() or Decimal('950.0')
        return monto / valor_dolar
    elif moneda_origen == 'USD' and moneda_destino == 'CLP':
        valor_dolar = obtener_valor_dolar() or Decimal('950.0')
        return monto * valor_dolar
    else:
        # Para otras conversiones, retornamos el mismo valor
        return monto
