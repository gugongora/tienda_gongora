from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.cart import get_cart_items, clear_cart
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from payments.webpay import crear_transaccion
from django.utils.crypto import get_random_string
from django.urls import reverse


@login_required
def checkout(request):
    cart_items = get_cart_items(request)
    if not cart_items:
        return redirect('store:product_list')

    total = sum(Decimal(item['subtotal']) for item in cart_items)

    if request.method == 'POST':
        # Crear orden
        order = Order.objects.create(
            user=request.user,
            total=total,
            status='pending'
        )

        # Agregar productos a la orden
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                subtotal=Decimal(item['subtotal'])
            )

        # Preparar datos para Webpay
        session_id = str(request.user.id)
        buy_order = f"orden-{order.id}-{get_random_string(6)}"
        return_url = request.build_absolute_uri(reverse('payments:webpay_confirmacion'))

        resultado = crear_transaccion(session_id, total, buy_order, return_url)

        # Guardar token y buy_order en la orden
        order.token = resultado["token"]
        order.buy_order = buy_order
        order.save()

        return redirect(f"{resultado['url']}?token_ws={resultado['token']}")

    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user:
        return redirect('store:product_list')

    return render(request, 'orders/order_confirmation.html', {'order': order})
