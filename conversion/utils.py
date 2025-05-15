import requests
from datetime import datetime

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
