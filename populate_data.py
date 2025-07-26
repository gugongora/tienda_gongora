import os
import django
import random
from decimal import Decimal

# Configurar el entorno de Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_gongora.settings')
django.setup()

from productos.models import Categoria, Marca, Producto, Precio
from operaciones.models import Sucursal, Stock, Pedido, DetallePedido
from django.contrib.auth.models import User, Group

def create_categories():
    categories = [
        {'nombre': 'Anillos', 'descripcion': 'Anillos de compromiso, boda y moda'},
        {'nombre': 'Collares', 'descripcion': 'Collares finos y colgantes elegantes'},
        {'nombre': 'Aros', 'descripcion': 'Aros clásicos, modernos y de fantasía'},
    ]
    for category in categories:
        Categoria.objects.get_or_create(
            nombre=category['nombre'],
            defaults={'descripcion': category['descripcion']}
        )
    print(f"✅ {len(categories)} categorías creadas")
    return Categoria.objects.all()

def create_brands():
    brands = [
        'Góngora Joyería', 'Platería Mapuche', 'Brillos del Sur',
        'Alhajas Reales', 'Joyas Licanray', 'Orfebrería Ñielol'
    ]
    for brand_name in brands:
        Marca.objects.get_or_create(nombre=brand_name)
    print(f"✅ {len(brands)} marcas creadas")
    return Marca.objects.all()

def create_products(categories, brands):
    products = [
        {'nombre': 'Anillo de Plata 950', 'categoria': 'Anillos', 'marca': 'Góngora Joyería', 'precio': '35000'},
        {'nombre': 'Anillo con Piedra Lapislázuli', 'categoria': 'Anillos', 'marca': 'Platería Mapuche', 'precio': '42000'},
        {'nombre': 'Collar de Cuarzo Rosa', 'categoria': 'Collares', 'marca': 'Brillos del Sur', 'precio': '28000'},
        {'nombre': 'Collar de Plata con Dije de Sol', 'categoria': 'Collares', 'marca': 'Joyas Licanray', 'precio': '39000'},
        {'nombre': 'Aros de Plata Filigrana', 'categoria': 'Aros', 'marca': 'Orfebrería Ñielol', 'precio': '33000'},
        {'nombre': 'Aros Colgantes Piedra Volcánica', 'categoria': 'Aros', 'marca': 'Brillos del Sur', 'precio': '31000'},
        {'nombre': 'Anillo de Oro Laminado', 'categoria': 'Anillos', 'marca': 'Alhajas Reales', 'precio': '45000'},
        {'nombre': 'Collar Doble Cadena con Perlas', 'categoria': 'Collares', 'marca': 'Alhajas Reales', 'precio': '37000'},
        {'nombre': 'Aros Argollas Grandes', 'categoria': 'Aros', 'marca': 'Joyas Licanray', 'precio': '25000'},
    ]

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
                'descripcion': f"Joya artesanal: {product['nombre']}. Hecha a mano en Chile.",
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

def create_stock(branches, products):
    for branch in branches:
        for product in products:
            Stock.objects.get_or_create(
                sucursal=branch,
                producto=product,
                defaults={'cantidad': random.randint(5, 50)}
            )
    print(f"✅ Inventario creado para {branches.count()} sucursales y {products.count()} productos")

def create_users_and_groups():
    grupo_personal, created = Group.objects.get_or_create(name='personal_interno')
    if created:
        print("✅ Grupo 'personal_interno' creado")
    
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
    for i in range(5):
        sucursal = random.choice(branches)
        pedido = Pedido.objects.create(
            sucursal=sucursal,
            estado=random.choice(['pendiente', 'aprobado', 'enviado']),
            notas=f"Pedido de prueba #{i+1} para {sucursal.nombre}"
        )
        productos_seleccionados = random.sample(list(products), random.randint(1, 5))
        for producto in productos_seleccionados:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=random.randint(1, 10)
            )
    print(f"✅ 5 pedidos de muestra creados")

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

if __name__ == '__main__':
    populate()
