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
        {'nombre': 'Herramientas Eléctricas', 'descripcion': 'Herramientas que funcionan con electricidad'},
        {'nombre': 'Herramientas Manuales', 'descripcion': 'Herramientas que no requieren electricidad'},
        {'nombre': 'Plomería', 'descripcion': 'Materiales y herramientas para plomería'},
        {'nombre': 'Electricidad', 'descripcion': 'Materiales para instalaciones eléctricas'},
        {'nombre': 'Pintura', 'descripcion': 'Pinturas y accesorios'},
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
        {'nombre': 'Taladro Inalámbrico', 'categoria': 'Herramientas Eléctricas', 'marca': 'DeWalt', 'precio': '899.99'},
        {'nombre': 'Sierra Circular', 'categoria': 'Herramientas Eléctricas', 'marca': 'Makita', 'precio': '1299.50'},
        {'nombre': 'Juego de Destornilladores', 'categoria': 'Herramientas Manuales', 'marca': 'Stanley', 'precio': '349.99'},
        {'nombre': 'Martillo de Carpintero', 'categoria': 'Herramientas Manuales', 'marca': 'Truper', 'precio': '149.50'},
        {'nombre': 'Tubo PVC 1"', 'categoria': 'Plomería', 'marca': 'Rotoplas', 'precio': '45.99'},
        {'nombre': 'Llave Ajustable 10"', 'categoria': 'Plomería', 'marca': 'Urrea', 'precio': '219.99'},
        {'nombre': 'Cable THW Cal. 12', 'categoria': 'Electricidad', 'marca': 'Steren', 'precio': '8.99'},
        {'nombre': 'Interruptor Sencillo', 'categoria': 'Electricidad', 'marca': 'Steren', 'precio': '39.99'},
        {'nombre': 'Pintura Vinílica 4L', 'categoria': 'Pintura', 'marca': 'Comex', 'precio': '499.99'},
        {'nombre': 'Brocha 2"', 'categoria': 'Pintura', 'marca': 'Pretul', 'precio': '29.99'},
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