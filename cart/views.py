from django.shortcuts import render, redirect, get_object_or_404
from productos.models import Producto  # ← CORREGIDO: usamos el modelo correcto
from django.contrib import messages

def add_to_cart(request, product_id):
    product = get_object_or_404(Producto, id=product_id)  # ← CORREGIDO
    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1

    request.session['cart'] = cart
    messages.success(request, f"“{product.nombre}” se ha agregado al carrito.")  # ← usamos .nombre
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Producto, id=int(product_id_str))  # ← CORREGIDO
        subtotal = product.precios.first().valor * quantity  # ← usamos precios[0]
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('cart:view_cart')

def remove_all_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'cart:view_cart'))

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    return redirect('cart:view_cart')
