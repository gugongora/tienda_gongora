# populate_data.py
import os
import django
import random
from decimal import Decimal

# Configurar el entorno de Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_gongora.settings')
django.setup()

# Importación de modelos necesarios desde las apps del proyecto
from productos.models import Categoria, Marca, Producto, Precio
from operaciones.models import Sucursal, Stock, Pedido, DetallePedido
from django.contrib.auth.models import User, Group

# Función para crear categorías de ejemplo
def create_categories():
    categories = [
        {'nombre': 'Herramientas Manuales', 'descripcion': 'Incluye herramientas eléctricas y manuales'},
        {'nombre': 'Materiales Básicos', 'descripcion': 'Materiales para construcción y acabados'},
        {'nombre': 'Equipos de Seguridad', 'descripcion': 'Equipos de protección personal y accesorios'},
    ]
    
    # Crear cada categoría si no existe
    for category in categories:
        Categoria.objects.get_or_create(
            nombre=category['nombre'],
            defaults={'descripcion': category['descripcion']}
        )
    
    print(f"✅ {len(categories)} categorías creadas")
    return Categoria.objects.all()

# Función para crear marcas de ejemplo
def create_brands():
    brands = [
        'DeWalt', 'Bosch', 'Makita', 'Stanley', 'Truper', 
        'Pretul', 'Rotoplas', 'Urrea', 'Steren', 'Comex'
    ]
    
    for brand_name in brands:
        Marca.objects.get_or_create(nombre=brand_name)
    
    print(f"✅ {len(brands)} marcas creadas")
    return Marca.objects.all()

# Función para crear productos con sus precios
def create_products(categories, brands):
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
    
    # Crear producto y su precio si no existe
    for idx, product in enumerate(products):
        categoria = Categoria.objects.get(nombre=product['categoria'])
        marca = Marca.objects.get(nombre=product['marca'])

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

        if created:
            Precio.objects.create(
                producto=producto,
                valor=Decimal(product['precio'])
            )
    
    print(f"✅ {len(products)} productos creados con sus precios")
    return Producto.objects.all()

# Función para crear sucursales de ejemplo
def create_branches():
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

# Función para asignar stock aleatorio a cada producto en cada sucursal
def create_stock(branches, products):
    for branch in branches:
        for product in products:
            Stock.objects.get_or_create(
                sucursal=branch,
                producto=product,
                defaults={'cantidad': random.randint(5, 50)}
            )
    
    print(f"✅ Inventario creado para {branches.count()} sucursales y {products.count()} productos")

# Función para crear usuarios y asignarlos a un grupo
def create_users_and_groups():
    grupo_personal, created = Group.objects.get_or_create(name='personal_interno')
    if created:
        print("✅ Grupo 'personal_interno' creado")
    
    # Crear usuario por cada sucursal
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

# Función para crear pedidos con detalles aleatorios
def create_sample_orders(branches, products):
    for i in range(5):  # Crear 5 pedidos
        sucursal = random.choice(branches)
        
        pedido = Pedido.objects.create(
            sucursal=sucursal,
            estado=random.choice(['pendiente', 'aprobado', 'enviado']),
            notas=f"Pedido de prueba #{i+1} para {sucursal.nombre}"
        )
        
        num_productos = random.randint(1, 5)
        productos_seleccionados = random.sample(list(products), num_productos)
        
        for producto in productos_seleccionados:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=random.randint(1, 10)
            )
    
    print(f"✅ 5 pedidos de muestra creados")

# Función principal que ejecuta todo el proceso de poblar la base de datos
def populate():
    print("🚀 Iniciando población de datos de prueba...")
    
    categorias = create_categories()
    marcas = create_brands()
    productos = create_products(categorias, marcas)
    sucursales = create_branches()
    
    create_stock(sucursales, productos)
    create_users_and_groups()
    create_sample_orders(sucursales, productos)
    
    print("\n✨ Datos de prueba creados exitosamente!")
    print("\nCredenciales para acceder a la API:")
    for user in User.objects.filter(groups__name='personal_interno'):
        print(f"- Usuario: {user.username}, Contraseña: contraseña123")

# Ejecutar el script solo si se llama directamente
if __name__ == '__main__':
    populate()
