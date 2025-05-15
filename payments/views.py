from django.shortcuts import render
from django.shortcuts import redirect
from .webpay import crear_transaccion
import requests
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse

from .webpay_conf import WEBPAY_API_BASE_URL, WEBPAY_API_KEY_ID, WEBPAY_API_KEY_SECRET

def iniciar_pago(request):
    # Simula datos de compra
    session_id = str(request.user.id if request.user.is_authenticated else "session_test")

    amount = 19990
    buy_order = "orden123"

    resultado = crear_transaccion(session_id, amount, buy_order)

    # Redirige al formulario de pago
    return redirect(resultado["url"] + "?token_ws=" + resultado["token"])





def webpay_confirmacion(request):
    token = request.GET.get("token_ws")

    if not token:
        return HttpResponse("Token no recibido", status=400)

    url = f"{WEBPAY_API_BASE_URL}/transactions/{token}"
    headers = {
        "Tbk-Api-Key-Id": WEBPAY_API_KEY_ID,
        "Tbk-Api-Key-Secret": WEBPAY_API_KEY_SECRET,
        "Content-Type": "application/json"
    }

    response = requests.put(url, headers=headers)
    data = response.json()

    print(data)
    
    # Aquí decides si mostrar éxito o error
    if data.get("status") == "AUTHORIZED":
        return HttpResponse("Pago exitoso")
    else:
        return HttpResponse(f"Pago fallido: {data.get('response_code', 'Error desconocido')}", status=400)