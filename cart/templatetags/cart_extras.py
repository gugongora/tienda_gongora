from django import template
from store.models import Product

register = template.Library()

@register.filter
def get_product(product_id):
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
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