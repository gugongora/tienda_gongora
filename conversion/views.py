from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .utils import get_usd_exchange_rate

def clp_to_usd_view(request):
    amount = request.GET.get('amount')
    try:
        amount = float(amount)
        result = get_usd_exchange_rate(amount)
        if result is not None:
            return JsonResponse({'clp': amount, 'usd': result})
    except:
        pass
    return JsonResponse({'error': 'No se pudo convertir'}, status=500)