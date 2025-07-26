from django.contrib import admin
from .models import Categoria, Marca, Producto, Precio
from django.utils.html import format_html

# Formulario embebido para los precios
class PrecioInline(admin.TabularInline):
    model = Precio
    extra = 1

# Admin para Producto con vista previa de imagen
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'marca', 'categoria', 'preview_imagen')
    list_filter = ('marca', 'categoria')
    search_fields = ('codigo', 'nombre', 'descripcion')
    inlines = [PrecioInline]

    def preview_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.imagen.url)
        return "Sin imagen"
    preview_imagen.short_description = 'Imagen'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
