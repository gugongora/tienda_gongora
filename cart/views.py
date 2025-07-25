# cart/views.py
import requests
from decimal import Decimal
from .cart import get_cart_items
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from types import SimpleNamespace

API_BASE_URL = "http://52.55.129.100/api/productos/"

def fetch_product_from_api(product_id):
    response = requests.get(f"{API_BASE_URL}{product_id}/")
    if response.status_code == 200:
        data = response.json()
        # Asegurarse de que el ID esté incluido
        data['id'] = int(product_id)
        return SimpleNamespace(**data)
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
    cart_items = get_cart_items(request)
    total = sum(item['subtotal'] for item in cart_items)

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
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