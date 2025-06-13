from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Category, Product
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class StoreTests(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Crear grupo de personal interno
        self.internal_group = Group.objects.create(name='personal_interno')
        self.user.groups.add(self.internal_group)
        
        # Crear categoría de prueba
        self.category = Category.objects.create(name='Herramientas')
        
        # Crear producto de prueba
        self.product = Product.objects.create(
            name='Martillo',
            description='Martillo de acero',
            price=Decimal('29.99'),
            category=self.category
        )
        
        # Cliente para pruebas
        self.client = Client()

    def test_product_creation(self):
        """Prueba la creación de un producto"""
        self.assertEqual(self.product.name, 'Martillo')
        self.assertEqual(self.product.price, Decimal('29.99'))
        self.assertEqual(self.product.category, self.category)

    def test_product_list_view(self):
        """Prueba la vista de lista de productos"""
        response = self.client.get(reverse('store:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product_list.html')

    def test_dashboard_access(self):
        """Prueba el acceso al dashboard interno"""
        # Primero intentamos acceder sin login
        response = self.client.get(reverse('store:dashboard_interno'))
        self.assertEqual(response.status_code, 302)  # Redirección al login
        
        # Luego intentamos con login
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('store:dashboard_interno'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/dashboard_interno.html')

    def test_category_creation(self):
        """Prueba la creación de una categoría"""
        category = Category.objects.create(name='Pinturas')
        self.assertEqual(category.name, 'Pinturas')
        self.assertEqual(str(category), 'Pinturas')  # Prueba el método __str__

    def tearDown(self):
        # Limpiar archivos de prueba
        if self.product.image:
            self.product.image.delete()
