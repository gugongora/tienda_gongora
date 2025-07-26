import requests
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from types import SimpleNamespace
from productos.models import Producto
from django.conf import settings
from utils.api import build_api_url
from .cart import Cart  # ✅ usamos la clase Cart

def fetch_product_from_api(product_id):
    if settings.DEBUG:
        try:
            producto = Producto.objects.get(id=product_id)
            precios = producto.precios.order_by('-fecha')
            precio_actual = precios.first().valor if precios.exists() else None

            return SimpleNamespace(
                id=producto.id,
                nombre=producto.nombre,
                descripcion=producto.descripcion,
                precio_actual=precio_actual,
                imagen=producto.imagen.url if producto.imagen else None,
            )
        except Producto.DoesNotExist:
            raise Http404("Producto no encontrado (modo DEBUG)")
    else:
        url = build_api_url(f"productos/{product_id}/")
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            data['id'] = int(product_id)
            data['precio_actual'] = Decimal(str(data.get('precio_actual', 0)))
            return SimpleNamespace(**data)
        except requests.RequestException as e:
            print(f"❌ Error al obtener producto desde la API: {e}")
            raise Http404("Producto no encontrado")


def add_to_cart(request, product_id):
    try:
        product = fetch_product_from_api(product_id)
    except Http404:
        messages.error(request, "Producto no encontrado.")
        return redirect('store:product_list')

    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart

    messages.success(request, f"“{product.nombre}” se ha agregado al carrito.")
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))


def view_cart(request):
    cart = Cart(request)
    cart_items = list(cart)
    total = cart.get_total_price()

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]
    request.session['cart'] = cart
    return redirect('cart:view_cart')


def remove_all_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'cart:view_cart'))


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + 1
    request.session['cart'] = cart
    return redirect('cart:view_cart')
