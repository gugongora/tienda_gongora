from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
import requests
import json
# Función para verificar si un usuario pertenece al grupo 'personal_interno'
def is_internal_person(user):
    return user.groups.filter(name='personal_interno').exists()

def product_list(request):
    categoria_id = request.GET.get('categoria')
    marca_id = request.GET.get('marca')

    products = Product.objects.all()

    if categoria_id:
        products = products.filter(categoria_id=categoria_id)
    if marca_id:
        products = products.filter(marca_id=marca_id)

    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

def search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'store/search_results.html', {'results': results, 'query': query})

@login_required
@user_passes_test(is_internal_person)
def dashboard_interno(request):
    stock_data = None
    pedido_detalle = None
    pedido_resultado = None

    # Preparar sesión y headers compartidos
    session = requests.Session()
    session.cookies.update(request.COOKIES)

    headers = {'Content-Type': 'application/json'}
    if 'csrftoken' in request.COOKIES:
        headers['X-CSRFToken'] = request.COOKIES['csrftoken']

    if request.method == 'POST':

        # --- CONSULTAR STOCK ---
        if 'consultar_stock' in request.POST:
            sucursal_id = request.POST.get('sucursal_id')
            if sucursal_id:
                url = f'http://127.0.0.1:8000/api/sucursales/{sucursal_id}/stock/'
                try:
                    response = session.get(url, headers=headers)
                    if response.status_code == 200:
                        stock_data = response.json() or {'mensaje': 'No hay stock disponible.'}
                    else:
                        stock_data = {
                            'error': f'Status {response.status_code}',
                            'detalle': response.text
                        }
                except requests.RequestException as e:
                    stock_data = {'error': f'Error en la solicitud: {str(e)}'}

        # --- CONSULTAR PEDIDO ---
        elif 'consultar_pedido' in request.POST:
            pedido_id = request.POST.get('pedido_id')
            if pedido_id:
                url = f'http://127.0.0.1:8000/api/pedidos/{pedido_id}/'
                try:
                    response = session.get(url, headers=headers)
                    if response.status_code == 200:
                        pedido_detalle = response.json()
                    else:
                        pedido_detalle = {
                            'error': f'Status {response.status_code}',
                            'detalle': response.text
                        }
                except requests.RequestException as e:
                    pedido_detalle = {'error': f'Error en la solicitud: {str(e)}'}

        # --- REALIZAR PEDIDO ---
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
                        codigo = codigo.strip()
                        cantidad = cantidad.strip()

                        try:
                            producto = Product.objects.get(codigo=codigo)
                            productos_items.append({
                                'producto_id': producto.id,
                                'cantidad': int(cantidad)
                            })
                        except Product.DoesNotExist:
                            errores.append(f'Producto "{codigo}" no encontrado.')
                        except ValueError:
                            errores.append(f'Cantidad inválida para producto "{codigo}".')

                if errores:
                    pedido_resultado = {'error': 'Errores al procesar productos', 'detalle': errores}
                else:
                    pedido_data = {
                        'sucursal_origen': int(sucursal_origen),
                        'items': productos_items,
                        'observaciones': observaciones
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
                            pedido_resultado = {
                                'error': f'Status {response.status_code}',
                                'detalle': response.text
                            }
                    except requests.RequestException as e:
                        pedido_resultado = {'error': f'Error al enviar pedido: {str(e)}'}

    context = {
        'product_list_url': reverse('store:product_list'),
        'stock_data': stock_data,
        'pedido_detalle': pedido_detalle,
        'pedido_resultado': pedido_resultado,
    }

    return render(request, 'store/dashboard_interno.html', context)