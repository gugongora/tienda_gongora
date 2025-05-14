from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    if str(product.id) in cart:  # Convertir el id del producto a cadena para evitar problemas de tipo
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1

    request.session['cart'] = cart
    return redirect('cart:view_cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))  # Convertimos product_id de nuevo a entero
        subtotal = product.price * quantity
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
    product_id_str = str(product_id)  # Convierte product_id a cadena

    print(f"Carrito antes de eliminar: {cart}")
    if product_id_str in cart:
        del cart[product_id_str]
        print(f"Producto {product_id} eliminado")
    else:
        print(f"Producto {product_id} no encontrado en el carrito")
    
    request.session['cart'] = cart
    print(f"Carrito después de eliminar: {cart}")

    return redirect('cart:view_cart')