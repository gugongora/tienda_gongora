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
    categoria_id = request.GET.get('categoria')
    marca_id = request.GET.get('marca')

    products = Product.objects.all()
    if categoria_id:
        print("✅ Filtro aplicado: categoría", categoria_id)
        products = products.filter(category_id=categoria_id)
    if marca_id:
        print("✅ Filtro aplicado: marca", marca_id)
        products = products.filter(brand_id=marca_id)

    return render(request, 'store/product_list.html', {'products': products})

# Vista para detalle de producto desde API externa
def product_detail(request, product_id):
    response = requests.get(f'http://127.0.0.1:8000/api/productos/{product_id}')
    if response.status_code == 200:
        product_data = response.json()
        product_data['id'] = product_id
        return render(request, 'store/product_detail.html', {'product': product_data})
    else:
        return render(request, 'store/product_detail.html', {'product': None})

# Vista para búsqueda de productos por nombre
def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/search_results.html', {'results': results, 'query': query})

# Dashboard protegido para grupo 'personal_interno'
@login_required
@user_passes_test(is_internal_person)
def dashboard_interno(request):
    stock_data = None
    pedido_detalle = None
    pedido_resultado = None
    sucursales = []

    # Inicia la sesión HTTP con cookies del usuario
    session = requests.Session()
    session.cookies.update(request.COOKIES)

    headers = {'Content-Type': 'application/json'}
    if 'csrftoken' in request.COOKIES:
        headers['X-CSRFToken'] = request.COOKIES['csrftoken']

    # Obtener sucursales desde API autenticada
    try:
        suc_response = session.get("http://127.0.0.1:8000/api/sucursales/", headers=headers)
        if suc_response.status_code == 200:
            data = suc_response.json()
            sucursales = data.get("results", [])
            print("⚙️ DEBUG: Sucursales cargadas:", sucursales)
        else:
            print(f"⚠️ ERROR: Status al obtener sucursales: {suc_response.status_code}")
    except Exception as e:
        print(f"❌ Excepción al obtener sucursales: {e}")

    # Procesamiento de formularios POST
    if request.method == 'POST':
        if 'consultar_stock' in request.POST:
            sucursal_id = request.POST.get('sucursal_id')
            if sucursal_id:
                url = f'hhttp://127.0.0.1:8000/api/sucursales/{sucursal_id}/stock/'
                try:
                    response = session.get(url, headers=headers)
                    if response.status_code == 200:
                        stock_data = response.json() or {'mensaje': 'No hay stock disponible.'}
                    else:
                        stock_data = {'error': f'Status {response.status_code}', 'detalle': response.text}
                except requests.RequestException as e:
                    stock_data = {'error': f'Error en la solicitud: {str(e)}'}

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

        elif 'realizar_pedido' in request.POST:
            sucursal_origen = request.POST.get('sucursal_origen')
            productos_str = request.POST.get('productos')
            observaciones = request.POST.get('observaciones', '')

            if not (sucursal_origen and productos_str):
                pedido_resultado = {'error': 'Debe completar todos los campos obligatorios.'}
            else:
                productos_items = []
                errores = []

                for item in productos_str.split(','):
                    if ':' in item:
                        codigo, cantidad = item.strip().split(':', 1)
                        try:
                            producto = Product.objects.get(codigo=codigo.strip())
                            productos_items.append({
                                'producto_codigo': producto.id,
                                'cantidad': int(cantidad.strip())
                            })
                        except Product.DoesNotExist:
                            errores.append(f'Producto "{codigo}" no encontrado.')
                        except ValueError:
                            errores.append(f'Cantidad inválida para "{codigo}".')

                if errores:
                    pedido_resultado = {'error': 'Errores al procesar productos', 'detalle': errores}
                else:
                    pedido_data = {
                        'sucursal_id': int(sucursal_origen),
                        'notas': observaciones,
                        'detalles': productos_items
                    }
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

    context = {
        'sucursales': sucursales,
        'stock_data': stock_data,
        'pedido_detalle': pedido_detalle,
        'pedido_resultado': pedido_resultado,
    }

    return render(request, 'store/dashboard_interno.html', context)