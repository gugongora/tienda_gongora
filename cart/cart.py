import requests
from decimal import Decimal
from django.http import Http404

API_BASE_URL = "http://127.0.0.1:8000/api/productos/"

def fetch_product_from_api(product_id):
    response = requests.get(f"{API_BASE_URL}{product_id}/")
    if response.status_code == 200:
        return response.json()
    raise Http404("Producto no encontrado")

def get_cart_items(request):
    cart = request.session.get('cart', {})
    items = []

    for product_id_str, quantity in cart.items():
        try:
            product_data = fetch_product_from_api(product_id_str)
            precios = product_data.get('precios', [])
            precio_actual = Decimal(precios[0]['valor']) if precios else Decimal(0)
            subtotal = precio_actual * quantity

            items.append({
                'product_id': int(product_id_str),
                'product_name': product_data['nombre'],
                'quantity': quantity,
                'subtotal': subtotal
            })

        except Http404:
            continue

    return items
