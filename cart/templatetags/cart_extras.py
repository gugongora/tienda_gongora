from django import template
from productos.models import Producto  # ✅ Corrección aquí

register = template.Library()

@register.filter
def get_product(product_id):
    try:
        return Producto.objects.get(id=int(product_id))  # Asegura que sea int
    except (Producto.DoesNotExist, ValueError, TypeError):
        return None

@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

@register.simple_tag(takes_context=True)
def cart_count(context):
    request = context['request']
    cart = request.session.get('cart', {})
    return sum(cart.values())
