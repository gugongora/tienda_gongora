from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
import requests
import json
from django.http import Http404

# Función para verificar si el usuario pertenece al grupo 'personal_interno'
def is_internal_person(user):
    return user.groups.filter(name='personal_interno').exists()

# Vista para listar productos, con filtros opcionales por categoría y marca
def product_list(request):
    categoria_id = request.GET.get('categoria')  # Obtiene el filtro por categoría (si existe)
    marca_id = request.GET.get('marca')          # Obtiene el filtro por marca (si existe)

    products = Product.objects.all()             # Obtiene todos los productos

    # Aplica los filtros si se han proporcionado
    if categoria_id:
        products = products.filter(categoria_id=categoria_id)
    if marca_id:
        products = products.filter(marca_id=marca_id)

    # Renderiza la plantilla con los productos filtrados
    return render(request, 'store/product_list.html', {'products': products})

import requests
from django.shortcuts import render

def product_detail(request, product_id):
    response = requests.get(f'http://127.0.0.1:8000/api/productos/{product_id}/')
    if response.status_code == 200:
        product_data = response.json()
        product_data['id'] = product_id  # ← asegúrate de pasar 'id' explícitamente
        return render(request, 'store/product_detail.html', {'product': product_data})
    else:
        return render(request, 'store/product_detail.html', {'product': None})


# Vista para buscar productos por nombre
def search(request):
    query = request.GET.get('q')  # Obtiene la consulta desde la URL (por ejemplo ?q=nombre)
    results = Product.objects.filter(name__icontains=query) if query else []  # Búsqueda parcial insensible a mayúsculas
    return render(request, 'store/search_results.html', {'results': results, 'query': query})

# Vista protegida para usuarios del grupo 'personal_interno'
# Permite:
# - Consultar stock de una sucursal
# - Ver detalles de un pedido
# - Realizar un nuevo pedido
@login_required
@user_passes_test(is_internal_person)
def dashboard_interno(request):
    # Variables para almacenar resultados según la acción
    stock_data = None
    pedido_detalle = None
    pedido_resultado = None

    # Se inicia una sesión para realizar solicitudes HTTP
    session = requests.Session()
    session.cookies.update(request.COOKIES)  # Se incluyen las cookies del usuario

    headers = {'Content-Type': 'application/json'}
    # Se añade el token CSRF si está disponible
    if 'csrftoken' in request.COOKIES:
        headers['X-CSRFToken'] = request.COOKIES['csrftoken']

    # Si se envió el formulario (POST)
    if request.method == 'POST':

        # Sección para consultar el stock de una sucursal
        if 'consultar_stock' in request.POST:
            sucursal_id = request.POST.get('sucursal_id')
            if sucursal_id:
                url = f'http://127.0.0.1:8000/api/sucursales/{sucursal_id}/stock/'
                try:
                    response = session.get(url, headers=headers)
                    if response.status_code == 200:
                        stock_data = response.json() or {'mensaje': 'No hay stock disponible.'}
                    else:
                        stock_data = {'error': f'Status {response.status_code}', 'detalle': response.text}
                except requests.RequestException as e:
                    stock_data = {'error': f'Error en la solicitud: {str(e)}'}

        # Sección para consultar el detalle de un pedido
        elif 'consultar_pedido' in request.POST:
            pedido_id = request.POST.get('pedido_id')
            if pedido_id:
                url = f'http://127.0.0.1:8000/api/pedidos/{pedido_id}/'
                try:
                    response = session.get(url, headers=headers)
                    if response.status_code == 200:
                        pedido_detalle = response.json()
                    else:
                        pedido_detalle = {'error': f'Status {response.status_code}', 'detalle': response.text}
                except requests.RequestException as e:
                    pedido_detalle = {'error': f'Error en la solicitud: {str(e)}'}

        # Sección para realizar un nuevo pedido
        elif 'realizar_pedido' in request.POST:
            sucursal_origen = request.POST.get('sucursal_origen')
            productos_str = request.POST.get('productos')  # Formato esperado: "PROD-001:5, PROD-002:10"
            observaciones = request.POST.get('observaciones', '')

            # Validación básica de campos obligatorios
            if not (sucursal_origen and productos_str):
                pedido_resultado = {'error': 'Debe completar todos los campos obligatorios.'}
            else:
                productos_items = []
                errores = []

                # Se procesan los productos ingresados
                for item in productos_str.split(','):
                    if ':' in item:
                        codigo, cantidad = item.strip().split(':', 1)
                        codigo = codigo.strip()
                        cantidad = cantidad.strip()
                        try:
                            producto = Product.objects.get(codigo=codigo)  # Busca el producto por código
                            productos_items.append({
                                'producto_codigo': producto.id,  # Usa el ID del producto
                                'cantidad': int(cantidad)        # Convierte cantidad a entero
                            })
                        except Product.DoesNotExist:
                            errores.append(f'Producto "{codigo}" no encontrado.')
                        except ValueError:
                            errores.append(f'Cantidad inválida para producto "{codigo}".')

                # Si hubo errores, se notifican al usuario
                if errores:
                    pedido_resultado = {'error': 'Errores al procesar productos', 'detalle': errores}
                else:
                    # Si todo es válido, se arma el JSON del pedido
                    pedido_data = {
                        'sucursal_id': int(sucursal_origen),
                        'notas': observaciones,
                        'detalles': productos_items
                    }

                    # Se envía el pedido a la API
                    try:
                        response = session.post(
                            'http://127.0.0.1:8000/api/pedidos/',
                            data=json.dumps(pedido_data),
                            headers=headers
                        )
                        if response.status_code in [200, 201]:
                            pedido_resultado = response.json()
                        else:
                            pedido_resultado = {'error': f'Status {response.status_code}', 'detalle': response.text}
                    except requests.RequestException as e:
                        pedido_resultado = {'error': f'Error al enviar pedido: {str(e)}'}

    # Se pasan todos los resultados al contexto para renderizar en la plantilla
    context = {
        'stock_data': stock_data,
        'pedido_detalle': pedido_detalle,
        'pedido_resultado': pedido_resultado,
    }

    return render(request, 'store/dashboard_interno.html', context)
