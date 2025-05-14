from decimal import Decimal
from store.models import Product

def get_cart_items(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity
            })
        except Product.DoesNotExist:
            continue

    return cart_items

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']

