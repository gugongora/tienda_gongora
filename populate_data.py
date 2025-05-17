# populate_data.py
import os
import django
import random
from decimal import Decimal

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_gongora.settings')
django.setup()

# Importar los modelos
from productos.models import Categoria, Marca, Producto, Precio
from operaciones.models import Sucursal, Stock, Pedido, DetallePedido
from django.contrib.auth.models import User, Group

def create_categories():
    """Crea categorías de muestra"""
    categories = [
       {'nombre': 'Herramientas Manuales', 'descripcion': 'Incluye herramientas eléctricas y manuales'},
        {'nombre': 'Materiales Básicos', 'descripcion': 'Materiales para construcción y acabados'},
        {'nombre': 'Equipos de Seguridad', 'descripcion': 'Equipos de protección personal y accesorios'},
    ]
    
    for category in categories:
        Categoria.objects.get_or_create(
            nombre=category['nombre'],
            defaults={'descripcion': category['descripcion']}
        )
    
    print(f"✅ {len(categories)} categorías creadas")
    return Categoria.objects.all()

def create_brands():
    """Crea marcas de muestra"""
    brands = [
        'DeWalt', 'Bosch', 'Makita', 'Stanley', 'Truper', 
        'Pretul', 'Rotoplas', 'Urrea', 'Steren', 'Comex'
    ]
    
    for brand_name in brands:
        Marca.objects.get_or_create(nombre=brand_name)
    
    print(f"✅ {len(brands)} marcas creadas")
    return Marca.objects.all()

def create_products(categories, brands):
    """Crea productos de muestra"""
    products = [
        # Herramientas Manuales
        {'nombre': 'Martillo de Carpintero', 'categoria': 'Herramientas Manuales', 'marca': 'Truper', 'precio': '150.00'},
        {'nombre': 'Juego de Destornilladores', 'categoria': 'Herramientas Manuales', 'marca': 'Stanley', 'precio': '300.00'},
        {'nombre': 'Llave Ajustable 10"', 'categoria': 'Herramientas Manuales', 'marca': 'Urrea', 'precio': '220.00'},
        {'nombre': 'Taladro Inalámbrico', 'categoria': 'Herramientas Manuales', 'marca': 'DeWalt', 'precio': '900.00'},
        {'nombre': 'Sierra Circular', 'categoria': 'Herramientas Manuales', 'marca': 'Makita', 'precio': '1300.00'},
        {'nombre': 'Lijadora Orbital', 'categoria': 'Herramientas Manuales', 'marca': 'Bosch', 'precio': '850.00'},
        
        # Materiales Básicos
        {'nombre': 'Bolsa de Cemento 50kg', 'categoria': 'Materiales Básicos', 'marca': 'Comex', 'precio': '250.00'},
        {'nombre': 'Saco de Arena', 'categoria': 'Materiales Básicos', 'marca': 'Truper', 'precio': '70.00'},
        {'nombre': 'Ladrillos Rústicos', 'categoria': 'Materiales Básicos', 'marca': 'Truper', 'precio': '3.00'},
        {'nombre': 'Pintura Vinílica 4L', 'categoria': 'Materiales Básicos', 'marca': 'Comex', 'precio': '500.00'},
        {'nombre': 'Barniz Protector', 'categoria': 'Materiales Básicos', 'marca': 'Comex', 'precio': '200.00'},
        {'nombre': 'Cerámica para Piso', 'categoria': 'Materiales Básicos', 'marca': 'Truper', 'precio': '350.00'},
        
        # Equipos de Seguridad
        {'nombre': 'Casco de Seguridad', 'categoria': 'Equipos de Seguridad', 'marca': 'Pretul', 'precio': '120.00'},
        {'nombre': 'Guantes Antideslizantes', 'categoria': 'Equipos de Seguridad', 'marca': 'Pretul', 'precio': '60.00'},
        {'nombre': 'Lentes de Seguridad', 'categoria': 'Equipos de Seguridad', 'marca': 'Pretul', 'precio': '80.00'},
        {'nombre': 'Juego de Tornillos y Anclajes', 'categoria': 'Equipos de Seguridad', 'marca': 'Stanley', 'precio': '90.00'},
        {'nombre': 'Fijador Multiusos', 'categoria': 'Equipos de Seguridad', 'marca': 'Steren', 'precio': '75.00'},
        {'nombre': 'Cinta Métrica 5m', 'categoria': 'Equipos de Seguridad', 'marca': 'Stanley', 'precio': '55.00'},
    ]
    
    for idx, product in enumerate(products):
        # Buscar categoría y marca
        categoria = Categoria.objects.get(nombre=product['categoria'])
        marca = Marca.objects.get(nombre=product['marca'])
        
        # Crear producto
        codigo = f'PROD-{idx+1:03d}'
        codigo_fabricante = f'FAB-{marca.nombre[:3].upper()}-{idx+1:03d}'
        
        producto, created = Producto.objects.get_or_create(
            codigo=codigo,
            defaults={
                'codigo_fabricante': codigo_fabricante,
                'nombre': product['nombre'],
                'descripcion': f"Descripción detallada para {product['nombre']}",
                'marca': marca,
                'categoria': categoria,
            }
        )
        
        # Crear precio
        if created:
            Precio.objects.create(
                producto=producto,
                valor=Decimal(product['precio'])
            )
    
    print(f"✅ {len(products)} productos creados con sus precios")
    return Producto.objects.all()

def create_branches():
    """Crea sucursales de muestra"""
    branches = [
        {'nombre': 'Tienda Central', 'direccion': 'Calle Principal #123', 'telefono': '555-1234'},
        {'nombre': 'Sucursal Norte', 'direccion': 'Av. del Norte #456', 'telefono': '555-5678'},
        {'nombre': 'Sucursal Sur', 'direccion': 'Blvd. del Sur #789', 'telefono': '555-9012'},
    ]
    
    for branch in branches:
        Sucursal.objects.get_or_create(
            nombre=branch['nombre'],
            defaults={
                'direccion': branch['direccion'],
                'telefono': branch['telefono']
            }
        )
    
    print(f"✅ {len(branches)} sucursales creadas")
    return Sucursal.objects.all()

def create_stock(branches, products):
    """Crea inventario de muestra"""
    for branch in branches:
        for product in products:
            # Crear stock aleatorio entre 5 y 50 unidades
            stock, created = Stock.objects.get_or_create(
                sucursal=branch,
                producto=product,
                defaults={'cantidad': random.randint(5, 50)}
            )
    
    print(f"✅ Inventario creado para {branches.count()} sucursales y {products.count()} productos")

def create_users_and_groups():
    """Crea usuarios y grupos de muestra"""
    # Crear grupo para personal interno si no existe
    grupo_personal, created = Group.objects.get_or_create(name='personal_interno')
    if created:
        print("✅ Grupo 'personal_interno' creado")
    
    # Crear usuarios para sucursales
    sucursales = Sucursal.objects.all()
    for sucursal in sucursales:
        username = f"usuario_{sucursal.nombre.lower().replace(' ', '_')}"
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f"{username}@tiendagongora.com",
                'first_name': f"Usuario de {sucursal.nombre}"
            }
        )
        
        if created:
            user.set_password('contraseña123')
            user.save()
            user.groups.add(grupo_personal)
            print(f"✅ Usuario '{username}' creado y asignado al grupo 'personal_interno'")

def create_sample_orders(branches, products):
    """Crea pedidos de muestra"""
    for i in range(5):  # Crear 5 pedidos de muestra
        # Seleccionar una sucursal aleatoria
        sucursal = random.choice(branches)
        
        # Crear pedido
        pedido = Pedido.objects.create(
            sucursal=sucursal,
            estado=random.choice(['pendiente', 'aprobado', 'enviado']),
            notas=f"Pedido de prueba #{i+1} para {sucursal.nombre}"
        )
        
        # Crear detalles de pedido (entre 1 y 5 productos)
        num_productos = random.randint(1, 5)
        productos_seleccionados = random.sample(list(products), num_productos)
        
        for producto in productos_seleccionados:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=random.randint(1, 10)
            )
    
    print(f"✅ 5 pedidos de muestra creados")

def populate():
    """Función principal para poblar la base de datos"""
    print("🚀 Iniciando población de datos de prueba...")
    
    # Crear datos básicos
    categorias = create_categories()
    marcas = create_brands()
    productos = create_products(categorias, marcas)
    sucursales = create_branches()
    
    # Crear relaciones
    create_stock(sucursales, productos)
    create_users_and_groups()
    create_sample_orders(sucursales, productos)
    
    print("\n✨ Datos de prueba creados exitosamente!")
    print("\nCredenciales para acceder a la API:")
    for user in User.objects.filter(groups__name='personal_interno'):
        print(f"- Usuario: {user.username}, Contraseña: contraseña123")

if __name__ == '__main__':
    populate()