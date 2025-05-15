from django.shortcuts import render

from django.http import JsonResponse
from .utils import obtener_valor_dolar

def convertir_moneda(request):
    try:
        monto = float(request.GET.get("monto", 0))
    except ValueError:
        return JsonResponse({"error": "Monto inválido"}, status=400)

    valor_dolar = obtener_valor_dolar()
    if valor_dolar is None:
        return JsonResponse({"error": "No se pudo obtener el valor del dólar"}, status=500)

    resultado = monto * valor_dolar
    return JsonResponse({
        "monto_usd": monto,
        "valor_dolar_clp": valor_dolar,
        "monto_clp": round(resultado, 2)
    })



def convertir_moneda_template(request):
    context = {"monto_usd": None, "valor_dolar": None, "monto_clp": None, "error": None}

    if "monto" in request.GET:
        try:
            monto = float(request.GET.get("monto"))
            valor_dolar = obtener_valor_dolar()
            if valor_dolar:
                context["monto_usd"] = monto
                context["valor_dolar"] = valor_dolar
                context["monto_clp"] = round(monto * valor_dolar, 2)
            else:
                context["error"] = "No se pudo obtener el valor del dólar."
        except ValueError:
            context["error"] = "Monto inválido."

    return render(request, "conversion/convertir.html", context)