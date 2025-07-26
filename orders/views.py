from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.cart import Cart  # ✅ Usamos la clase Cart, no más get_cart_items
from django.contrib.auth.decorators import login_required, user_passes_test
from decimal import Decimal
from payments.webpay import crear_transaccion
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.core.paginator import Paginator  # Opcional para paginación
from django.contrib import messages


@login_required
def checkout(request):
    cart = Cart(request)
    cart_items = list(cart)

    if not cart_items:
        return redirect('store:product_list')

    total = cart.get_total_price()

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total=total,
            status='pending'
        )

        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                product_name=item['product'].nombre,
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

        request.session['cart'] = {}  # Vaciar carrito tras compra
        request.session.modified = True

        return redirect(f"{resultado['url']}?token_ws={resultado['token']}")

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user:
        return redirect('store:product_list')

    return render(request, 'orders/order_confirmation.html', {'order': order})


@login_required
def mis_pedidos(request):
    pedidos = Order.objects.filter(user=request.user).order_by('-created_at')
    
    paginator = Paginator(pedidos, 10)  # 10 pedidos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'orders/mis_pedidos.html', {
        'page_obj': page_obj
    })


def is_personal_interno(user):
    return user.groups.filter(name='personal_interno').exists()


@login_required
@user_passes_test(is_personal_interno)
def dashboard_pedidos(request):
    orders = Order.objects.select_related('user').order_by('-created_at')
    return render(request, 'orders/dashboard_pedidos.html', {'orders': orders})


@login_required
@user_passes_test(is_personal_interno)
def detalle_pedido(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    if request.method == 'POST' and request.user.groups.filter(name="personal_interno").exists():
        nuevo_estado = request.POST.get("status")
        if nuevo_estado in ['pending', 'paid', 'cancelled']:
            order.status = nuevo_estado
            order.save()
            messages.success(request, "Estado del pedido actualizado correctamente.")

        return redirect('orders:detalle_pedido', order_id=order.id)

    return render(request, 'orders/detalle_pedido.html', {
        'order': order,
        'items': items
    })
