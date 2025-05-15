import requests
from datetime import datetime, timedelta
from base64 import b64encode
from xml.etree import ElementTree as ET

# Credenciales de desarrollo
BCCH_API_USER = "gustavogongoraortiz@gmail.com"
BCCH_API_PASS = "@Eldiablo1"

def get_usd_exchange_rate():
    url = "https://si3.bcentral.cl/SieteWS/SieteWS.asmx"
    soap_action = "http://serviciosweb.siete.bcentral.cl/GetSeries"  # SOAPAction requerida

    fecha = (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y")
    serie_code = "F073.TCO.PRE.Z.D"

    soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <GetSeries xmlns="http://serviciosweb.siete.bcentral.cl">
          <codigoSerie>{serie_code}</codigoSerie>
          <fechaInicio>{fecha}</fechaInicio>
          <fechaFin>{fecha}</fechaFin>
          <codigoIdioma>es</codigoIdioma>
        </GetSeries>
      </soap:Body>
    </soap:Envelope>
    """

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": soap_action,  # ✅ NECESARIO
        "Authorization": "Basic " + b64encode(f"{BCCH_API_USER}:{BCCH_API_PASS}".encode()).decode()
    }

    try:
        response = requests.post(url, data=soap_body.encode("utf-8"), headers=headers)

        if response.status_code == 200:
            tree = ET.fromstring(response.content)
            value = tree.find('.//{http://serviciosweb.siete.bcentral.cl}OBS_VALOR')
            if value is not None:
                return float(value.text.replace(',', '.'))
            else:
                print("⚠️ No se encontró OBS_VALOR en la respuesta:")
                print(response.content.decode())
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")

    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

    return None
