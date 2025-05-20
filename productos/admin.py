# Importa el módulo de administración de Django
from django.contrib import admin

# Importa los modelos que se administrarán desde esta app
from .models import Categoria, Marca, Producto, Precio

# Define una clase en línea para mostrar los precios asociados a un producto dentro del mismo formulario en el admin
class PrecioInline(admin.TabularInline):
    model = Precio  # Modelo que se mostrará como formulario embebido
    extra = 1        # Muestra un formulario adicional vacío para agregar un nuevo precio fácilmente

# Configuración personalizada del panel de administración para el modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de productos del admin
    list_display = ('codigo', 'nombre', 'marca', 'categoria')
    
    # Filtros laterales por marca y categoría
    list_filter = ('marca', 'categoria')
    
    # Campos que se pueden buscar desde la barra de búsqueda del admin
    search_fields = ('codigo', 'nombre', 'descripcion')
    
    # Añade el formulario de precios embebido dentro del formulario de producto
    inlines = [PrecioInline]

# Configuración personalizada del panel de administración para el modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # Campos visibles en la lista de categorías
    list_display = ('nombre', 'descripcion')
    
    # Campos que se pueden buscar en el panel de admin
    search_fields = ('nombre',)

# Configuración personalizada del panel de administración para el modelo Marca
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    # Campo visible en la lista de marcas
    list_display = ('nombre',)
    
    # Campo por el cual se puede buscar
    search_fields = ('nombre',)
