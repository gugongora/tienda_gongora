import requests
from decimal import Decimal
from django.http import Http404

# Usar la URL base correcta de la API
API_BASE_URL = "http://127.0.0.1:8000/api/productos/"

def fetch_product_from_api(product_id):
    """
    Obtiene datos de un producto desde la API.
    Las pruebas de integración requieren que la API esté funcionando.
    """
    try:
        response = requests.get(f"{API_BASE_URL}{product_id}/", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            raise Http404("Producto no encontrado")
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        # Si la API no está disponible, las pruebas de integración fallarán
        # Esto es intencional para asegurar que la API esté funcionando
        raise Http404(f"No se pudo conectar a la API: {e}")

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
