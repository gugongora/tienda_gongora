from django import template
from cart.cart import Cart

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_count(context):
    """
    Retorna la cantidad total de productos en el carrito.
    """
    request = context['request']
    cart = Cart(request)
    return len(cart)

@register.simple_tag(takes_context=True)
def cart_total(context):
    """
    Retorna el total en pesos del carrito.
    """
    request = context['request']
    cart = Cart(request)
    return cart.get_total_price()
