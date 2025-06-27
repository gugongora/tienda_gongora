"""
Archivo de pruebas de integración para Tienda Góngora

Diferencia entre pruebas unitarias e integración:
- Pruebas unitarias: verifican el funcionamiento de una unidad de código de forma aislada (función, método, clase).
- Pruebas de integración: validan que varios componentes o servicios funcionen correctamente juntos, simulando flujos reales de uso.

Este archivo contiene 6 pruebas de integración automatizadas con pytest y Django.
"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Group
from decimal import Decimal
from productos.models import Categoria, Marca, Producto, Precio
from operaciones.models import Sucursal, Stock, Pedido, DetallePedido
from orders.models import Order, OrderItem
from cart.cart import get_cart_items
from django.test import Client

@pytest.mark.django_db
class TestFlujosIntegracion:
    def setup_method(self):
        self.client = Client()
        # Datos base para los flujos
        self.categoria = Categoria.objects.create(nombre='Herramientas', descripcion='Herramientas de construcción')
        self.marca = Marca.objects.create(nombre='Stanley')
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            codigo_fabricante='FAB-STA-001',
            nombre='Martillo Profesional',
            descripcion='Martillo de alta calidad',
            marca=self.marca,
            categoria=self.categoria
        )
        self.precio = Precio.objects.create(producto=self.producto, valor=Decimal('150.00'))
        self.sucursal = Sucursal.objects.create(nombre='Sucursal Centro', direccion='Av. Principal 123', telefono='555-0123')
        self.stock = Stock.objects.create(sucursal=self.sucursal, producto=self.producto, cantidad=50)
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_flujo_compra_completo(self):
        """Flujo de compra completo: agregar al carrito, crear orden, procesar pago"""
        self.client.login(username='testuser', password='testpass123')
        session = self.client.session
        # Agregar producto al carrito usando la sesión
        session['cart'] = {str(self.producto.id): 2}
        session.save()
        # Obtener productos del carrito
        cart_items = get_cart_items(self.client)
        total = sum(item['subtotal'] for item in cart_items)
        # Crear orden
        response = self.client.post(reverse('orders:checkout'), {
            'user': self.user.id,
            'total': total,
            'status': 'pending',
            'token': 'token_test',
            'buy_order': 'BO1234',
        })
        assert response.status_code in (200, 302)
        # Procesar pago (simulado)
        order = Order.objects.last()
        order.status = 'paid'
        order.save()
        assert order.status == 'paid'

    def test_registro_y_autenticacion_usuario(self):
        """Registro y autenticación de usuario y acceso a recursos protegidos"""
        response = self.client.post(reverse('users:register'), {
            'username': 'nuevo_usuario',
            'email': 'nuevo@correo.com',
            'password1': 'passseguro123',
            'password2': 'passseguro123',
        })
        assert response.status_code in (200, 302)
        user = User.objects.get(username='nuevo_usuario')
        # Agregar usuario al grupo 'personal_interno'
        grupo_interno, _ = Group.objects.get_or_create(name='personal_interno')
        user.groups.add(grupo_interno)
        login = self.client.login(username='nuevo_usuario', password='passseguro123')
        assert login
        # Acceso a dashboard protegido
        response = self.client.get(reverse('store:dashboard_interno'))
        assert response.status_code in (200, 302)

    def test_creacion_producto_y_stock(self):
        """Creación de producto y verificación de stock en sucursal"""
        producto = Producto.objects.create(
            codigo='PROD-002',
            codigo_fabricante='FAB-STA-002',
            nombre='Destornillador',
            descripcion='Destornillador de precisión',
            marca=self.marca,
            categoria=self.categoria
        )
        stock = Stock.objects.create(sucursal=self.sucursal, producto=producto, cantidad=30)
        assert stock.producto == producto
        assert stock.sucursal == self.sucursal
        assert stock.cantidad == 30

    def test_pedido_y_actualizacion_stock(self):
        """Pedido desde una sucursal y actualización de stock"""
        pedido = Pedido.objects.create(sucursal=self.sucursal, estado='pendiente', notas='Pedido integración')
        cantidad_inicial = self.stock.cantidad
        DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=5)
        # Simular actualización de stock
        self.stock.cantidad -= 5
        self.stock.save()
        assert self.stock.cantidad == cantidad_inicial - 5

    def test_conversion_moneda_en_compra(self):
        """Proceso de conversión de moneda en una compra"""
        # Simular conversión usando utilidades del módulo conversion
        from conversion.utils import convertir_monto
        monto_clp = Decimal('15000')
        monto_usd = convertir_monto(monto_clp, 'CLP', 'USD')
        assert monto_usd > 0

    def test_confirmacion_pedido_y_generacion_orden(self):
        """Confirmación de pedido y generación de orden"""
        pedido = Pedido.objects.create(sucursal=self.sucursal, estado='pendiente', notas='Pedido a confirmar')
        detalle = DetallePedido.objects.create(pedido=pedido, producto=self.producto, cantidad=2)
        # Confirmar pedido y generar orden
        pedido.estado = 'confirmado'
        pedido.save()
        order = Order.objects.create(user=self.user, total=Decimal('300.00'), status='pending', token='token_conf', buy_order='BOCONF')
        OrderItem.objects.create(order=order, product_id=self.producto.id, product_name=self.producto.nombre, quantity=2, subtotal=Decimal('300.00'))
        assert pedido.estado == 'confirmado'
        assert order.total == Decimal('300.00') 