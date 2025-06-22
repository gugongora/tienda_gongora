"""
6 Pruebas unitarias automatizadas para Tienda Góngora
Una prueba por cada componente clave del sistema
Ejecutar con: python manage.py test tests
"""

import os
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from decimal import Decimal

# Configurar Django para las pruebas
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_gongora.settings')
django.setup()

from store.models import Category, Product
from productos.models import Categoria, Marca, Producto, Precio
from operaciones.models import Sucursal, Stock, Pedido, DetallePedido
from orders.models import Order, OrderItem


class TestComponentesClave(TestCase):
    """6 Pruebas unitarias para los componentes clave del sistema"""
    
    def setUp(self):
        """Configuración inicial para todas las pruebas"""
        self.client = Client()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Crear grupo personal_interno
        self.grupo_interno = Group.objects.create(name='personal_interno')
        self.user.groups.add(self.grupo_interno)
        
        # Crear datos para productos
        self.categoria = Categoria.objects.create(
            nombre='Herramientas',
            descripcion='Herramientas de construcción'
        )
        self.marca = Marca.objects.create(nombre='Stanley')
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            codigo_fabricante='FAB-STA-001',
            nombre='Martillo Profesional',
            descripcion='Martillo de alta calidad',
            marca=self.marca,
            categoria=self.categoria
        )
        self.precio = Precio.objects.create(
            producto=self.producto,
            valor=Decimal('150.00')
        )
        
        # Crear datos para operaciones
        self.sucursal = Sucursal.objects.create(
            nombre='Sucursal Centro',
            direccion='Av. Principal 123',
            telefono='555-0123'
        )
        self.stock = Stock.objects.create(
            sucursal=self.sucursal,
            producto=self.producto,
            cantidad=50
        )
        
        # Crear datos para órdenes
        self.order = Order.objects.create(
            user=self.user,
            total=Decimal('250.00'),
            status='pending',
            token='test_token_123',
            buy_order='BO123'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product_id=self.producto.id,
            product_name=self.producto.nombre,
            quantity=5,
            subtotal=Decimal('250.00')
        )
    
    def test_1_creacion_producto_con_precio(self):
        """✅ Validación 1 – test_1_creacion_producto_con_precio
        📌 Valida que el producto tiene un precio asociado correctamente."""
        precio_actual = self.producto.precios.first()
        self.assertIsNotNone(precio_actual)
        self.assertEqual(precio_actual.valor, Decimal('150.00'))
    
    def test_2_gestion_stock_sucursal(self):
        """✅ Validación 2 – test_2_gestion_stock_sucursal
        📌 Verifica que el stock de un producto está correctamente asociado a la sucursal."""
        self.assertEqual(self.stock.sucursal, self.sucursal)
        self.assertEqual(self.stock.producto, self.producto)
        self.assertEqual(self.stock.cantidad, 50)
    
    def test_3_creacion_pedido_con_detalles(self):
        """✅ Validación 3 – test_3_creacion_pedido_con_detalles
        📌 Comprueba que un detalle de pedido se relaciona bien con el producto y el pedido."""
        pedido = Pedido.objects.create(
            sucursal=self.sucursal,
            estado='pendiente',
            notas='Pedido de prueba'
        )
        detalle = DetallePedido.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=10
        )
        self.assertEqual(detalle.pedido, pedido)
        self.assertEqual(detalle.producto, self.producto)
    
    def test_4_creacion_orden_con_items(self):
        """✅ Validación 4 – test_4_creacion_orden_con_items
        📌 Verifica que el total de la orden sea el correcto."""
        self.assertEqual(self.order.total, Decimal('250.00'))
        self.assertEqual(self.order_item.subtotal, Decimal('250.00'))
    
    def test_5_autenticacion_y_autorizacion(self):
        """✅ Validación 5 – test_5_autenticacion_y_autorizacion
        📌 Verifica que un usuario autenticado puede acceder al dashboard interno."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('store:dashboard_interno'))
        self.assertEqual(response.status_code, 200)
    
    def test_6_vista_lista_productos(self):
        """✅ Validación 6 – test_6_vista_lista_productos
        📌 Verifica que la vista de productos responde correctamente con filtro por categoría."""
        categoria2 = Category.objects.create(name='Herramientas')
        product2 = Product.objects.create(
            name='Destornillador',
            description='Destornillador Phillips',
            price=Decimal('50.00'),
            category=categoria2
        )
        response = self.client.get(
            reverse('store:product_list'),
            {'categoria': categoria2.id}
        )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    # Ejecutar las pruebas
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'test', 'tests']) 