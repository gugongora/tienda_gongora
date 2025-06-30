from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.cart import get_cart_items
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from payments.webpay import crear_transaccion
from django.utils.crypto import get_random_string
from django.urls import reverse
from types import SimpleNamespace
import requests


@login_required
def checkout(request):
    cart_items = get_cart_items(request)
    if not cart_items:
        return redirect('store:product_list')

    total = sum(Decimal(item['subtotal']) for item in cart_items)

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total=total,
            status='pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],  # Usamos ID directo
                product_name=item['product_name'],
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )

        session_id = str(request.user.id)
        buy_order = f"orden-{order.id}-{get_random_string(6)}"
        return_url = request.build_absolute_uri(reverse('payments:webpay_confirmacion'))

        resultado = crear_transaccion(session_id, total, buy_order, return_url)

        order.token = resultado["token"]
        order.buy_order = buy_order
        order.save()

        # Limpiar carrito
        request.session['cart'] = {}
        request.session.modified = True

        return redirect(f"{resultado['url']}?token_ws={resultado['token']}")

    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total': total})


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user:
        return redirect('store:product_list')

    return render(request, 'orders/order_confirmation.html', {'order': order})


def get_cart_items_from_api(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal(0)

    for product_id_str, quantity in cart.items():
        try:
            response = requests.get(f"54.208.45.218/api/productos/{product_id_str}/")
            if response.status_code != 200:
                continue
            data = response.json()
            product = SimpleNamespace(**data)
            precios = getattr(product, 'precios', [])
            precio_actual = Decimal(precios[0]['valor']) if precios else Decimal(0)
            subtotal = precio_actual * quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except:
            continue

    return cart_items, total