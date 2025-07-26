# cart_extras.py
from django import template
from productos.models import Producto
from types import SimpleNamespace

register = template.Library()

@register.filter
def to_int(value):
    try:
        return int(value)
    except:
        return 0

@register.simple_tag(takes_context=True)
def cart_total(context):
    request = context['request']
    cart = request.session.get('cart', {})
    total = 0
    for product_id, quantity in cart.items():
        try:
            producto = Producto.objects.get(id=product_id)
            precio = producto.precios.order_by('-fecha').first()
            valor = precio.valor if precio else 0
            total += valor * quantity
        except:
            continue
    return total

@register.filter
def get_product(product_id):
    try:
        producto = Producto.objects.get(id=product_id)
        precio = producto.precios.order_by('-fecha').first()
        return SimpleNamespace(
            id=producto.id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            imagen=producto.imagen.url if producto.imagen else None,
            precio_actual=precio.valor if precio else 0
        )
    except:
        return None
