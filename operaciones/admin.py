
# operaciones/admin.py
from django.contrib import admin
from .models import Sucursal, Stock, Pedido, DetallePedido, MensajeContacto

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')
    search_fields = ('nombre', 'direccion')
    inlines = [StockInline]

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'sucursal', 'fecha_creacion', 'estado')
    list_filter = ('estado', 'sucursal')
    search_fields = ('id', 'sucursal__nombre')
    inlines = [DetallePedidoInline]

@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha_creacion')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre', 'email', 'mensaje')
    readonly_fields = ('fecha_creacion',)