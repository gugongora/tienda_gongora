import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from orders.models import Order
from .webpay_conf import WEBPAY_API_BASE_URL, WEBPAY_API_KEY_ID, WEBPAY_API_KEY_SECRET

# Diccionario de mensajes según response_code de Transbank
WEBPAY_RESPONSES = {
    0: "Transacción aprobada",
    -1: "Rechazo de la transacción",
    -2: "Transacción debe reintentarse",
    -3: "Error en transacción",
    -4: "Rechazo de transacción",
    -5: "Rechazo por error de tasa",
    -6: "Excede cupo máximo mensual",
    -7: "Excede límite diario por transacción",
    -8: "Rubro no autorizado",
}

def iniciar_pago(request):
    # Solo para pruebas directas (no se usa en checkout normal)
    session_id = str(request.user.id if request.user.is_authenticated else "anon")
    amount = 19990
    buy_order = "orden123"
    return_url = request.build_absolute_uri(reverse("payments:webpay_confirmacion"))
    resultado = crear_transaccion(session_id, amount, buy_order, return_url)
    return redirect(f"{resultado['url']}?token_ws={resultado['token']}")


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

    try:
        order = Order.objects.get(token=token)
    except Order.DoesNotExist:
        return HttpResponse("Orden no encontrada para el token", status=404)

    if data.get("status") == "AUTHORIZED":
        order.status = "paid"
        order.save()
        request.session['cart'] = {}  # Limpiar carrito después del pago
        return redirect('orders:order_confirmation', order_id=order.id)
    else:
        order.status = "cancelled"
        order.save()
        mensaje = WEBPAY_RESPONSES.get(data.get("response_code"), "Error desconocido")
        return render(request, "orders/payment_failed.html", {
            "order": order,
            "mensaje": mensaje,
            "detalle": data,
        })
