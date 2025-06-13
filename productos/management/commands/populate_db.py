from django.core.management.base import BaseCommand
from productos.models import Categoria, Marca, Producto
from decimal import Decimal

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        # Crear categorías
        categorias = [
            {'nombre': 'Herramientas'},
            {'nombre': 'Pinturas'},
            {'nombre': 'Construcción'},
        ]
        
        for cat_data in categorias:
            Categoria.objects.get_or_create(**cat_data)
            self.stdout.write(f'Categoría creada: {cat_data["nombre"]}')

        # Crear marcas
        marcas = [
            {'nombre': 'Stanley'},
            {'nombre': 'Truper'},
            {'nombre': 'Comex'},
        ]
        
        for marca_data in marcas:
            Marca.objects.get_or_create(**marca_data)
            self.stdout.write(f'Marca creada: {marca_data["nombre"]}')

        # Crear productos
        productos = [
            {
                'nombre': 'Martillo Profesional',
                'descripcion': 'Martillo de acero con mango ergonómico',
                'precio_actual': Decimal('29.99'),
                'codigo': 'MART-001',
                'categoria': Categoria.objects.get(nombre='Herramientas'),
                'marca': Marca.objects.get(nombre='Stanley')
            },
            {
                'nombre': 'Pintura Interior',
                'descripcion': 'Pintura para interiores, color blanco',
                'precio_actual': Decimal('45.99'),
                'codigo': 'PINT-001',
                'categoria': Categoria.objects.get(nombre='Pinturas'),
                'marca': Marca.objects.get(nombre='Comex')
            },
            {
                'nombre': 'Cemento Portland',
                'descripcion': 'Cemento gris para construcción',
                'precio_actual': Decimal('15.99'),
                'codigo': 'CEM-001',
                'categoria': Categoria.objects.get(nombre='Construcción'),
                'marca': Marca.objects.get(nombre='Truper')
            }
        ]
        
        for prod_data in productos:
            Producto.objects.get_or_create(codigo=prod_data['codigo'], defaults=prod_data)
            self.stdout.write(f'Producto creado: {prod_data["nombre"]}')

        self.stdout.write(self.style.SUCCESS('Base de datos poblada exitosamente')) 