# productos/admin.py
from django.contrib import admin
from .models import Categoria, Marca, Producto, Precio

class PrecioInline(admin.TabularInline):
    model = Precio
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'marca', 'categoria')
    list_filter = ('marca', 'categoria')
    search_fields = ('codigo', 'nombre', 'descripcion')
    inlines = [PrecioInline]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)