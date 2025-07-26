from decimal import Decimal
from django.http import Http404
from productos.models import Producto
from utils.api import build_api_url
import requests
from django.conf import settings
from types import SimpleNamespace


def fetch_product_from_api(product_id):
    if settings.DEBUG:
        try:
            producto = Producto.objects.get(id=product_id)
            precios = producto.precios.order_by('-fecha')
            precio_actual = precios.first().valor if precios.exists() else Decimal('0')

            return {
                'id': producto.id,
                'nombre': producto.nombre,
                'precio_actual': precio_actual,
                'imagen': str(producto.imagen.url) if hasattr(producto.imagen, 'url') else None,
            }
        except Producto.DoesNotExist:
            raise Http404("Producto no encontrado (modo DEBUG)")
    else:
        url = build_api_url(f"productos/{product_id}/")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            data['precio_actual'] = Decimal(str(data.get('precio_actual', 0)))
            return data
        except requests.RequestException as e:
            print(f"❌ Error al obtener producto desde la API: {e}")
            raise Http404("Producto no encontrado")


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def __iter__(self):
        for product_id_str, quantity in self.cart.items():
            try:
                product_data = fetch_product_from_api(product_id_str)
                precio_actual = product_data.get('precio_actual', Decimal('0'))
                subtotal = precio_actual * quantity

                yield {
                    'product': SimpleNamespace(**product_data),
                    'product_id': int(product_id_str),
                    'quantity': quantity,
                    'subtotal': subtotal,
                }
            except Http404:
                continue

    def __len__(self):
        return sum(self.cart.values())

    def get_total_price(self):
        return sum(item['subtotal'] for item in self)
