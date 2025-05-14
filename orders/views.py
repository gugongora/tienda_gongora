from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.cart import get_cart_items, clear_cart
from django.contrib.auth.decorators import login_required
from decimal import Decimal


@login_required
def create_order(request):
    cart_items = get_cart_items(request)
    if not cart_items:
        return redirect('product_list')

    # Crear la orden (sin necesidad de un usuario autenticado)
    order = Order.objects.create(user=request.user)  # Usamos request.user, pero este puede ser anónimo o un usuario genérico

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity']
        )

    clear_cart(request)
    return render(request, 'orders/order_confirmation.html', {'order': order})


def checkout(request):
    # Obtener los productos en el carrito
    cart_items = get_cart_items(request)
    total = sum(item['subtotal'] for item in cart_items)
    
    # Si el usuario no está logueado, redirigir a la página de login
    if not request.user.is_authenticated:
        return redirect('login')  # Suponiendo que tengas una vista de login
    
    # Si el formulario es enviado, procesar la orden
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total=Decimal(total),
            status='pending'
        )
        
        # Agregar los productos a la orden
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )

        # Limpiar el carrito después de realizar la compra
        request.session['cart'] = {}

        # Redirigir a una página de confirmación
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_confirmation.html', {'order': order})
