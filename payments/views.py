import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from orders.models import Order
from .webpay_conf import WEBPAY_API_BASE_URL, WEBPAY_API_KEY_ID, WEBPAY_API_KEY_SECRET

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

    try:
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        # Si falla la llamada a Webpay, muestra error limpio
        try:
            order = Order.objects.get(token=token)
            order.status = "cancelled"
            order.save()
        except Order.DoesNotExist:
            return HttpResponse("Orden no encontrada para el token", status=404)

        return render(request, "orders/payment_failed.html", {
            "order": order,
            "mensaje": "Error al confirmar el pago con Webpay (HTTP 500)",
            "detalle": str(err),
        })

    try:
        order = Order.objects.get(token=token)
    except Order.DoesNotExist:
        return HttpResponse("Orden no encontrada para el token", status=404)

    if data.get("status") == "AUTHORIZED":
        order.status = "paid"
        order.save()
        request.session['cart'] = {}
        return redirect('orders:order_confirmation', order_id=order.id)
    else:
        order.status = "cancelled"
        order.save()
        codigo = data.get("response_code")
        mensaje = WEBPAY_RESPONSES.get(codigo, f"Error desconocido (código: {codigo})")
        return render(request, "orders/payment_failed.html", {
            "order": order,
            "mensaje": mensaje,
            "detalle": data,
        })
