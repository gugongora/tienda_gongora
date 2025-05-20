# Importa el módulo de administración de Django
from django.contrib import admin

# Importa los modelos definidos en la app operaciones
from .models import Sucursal, Stock, Pedido, DetallePedido, MensajeContacto

# Configura un formulario embebido (inline) para el modelo Stock
# Esto permite agregar o editar el stock de una sucursal directamente desde su formulario en el panel de admin
class StockInline(admin.TabularInline):
    model = Stock      # Modelo relacionado a mostrar
    extra = 1          # Muestra un formulario vacío adicional para agregar nuevos registros fácilmente

# Configuración personalizada del panel de administración para el modelo Sucursal
@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de sucursales
    list_display = ('nombre', 'direccion', 'telefono')
    
    # Campos por los que se puede buscar en la barra superior
    search_fields = ('nombre', 'direccion')
    
    # Muestra el formulario de stock dentro del formulario de la sucursal
    inlines = [StockInline]

# Configura un formulario embebido (inline) para los detalles del pedido
# Permite agregar productos al pedido directamente desde el mismo formulario
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

# Configuración del panel de administración para el modelo Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de pedidos
    list_display = ('id', 'sucursal', 'fecha_creacion', 'estado')
    
    # Filtros laterales para buscar pedidos por estado o sucursal
    list_filter = ('estado', 'sucursal')
    
    # Permite buscar pedidos por ID y nombre de la sucursal (campo relacionado)
    search_fields = ('id', 'sucursal__nombre')
    
    # Muestra los detalles del pedido embebidos en el formulario del pedido
    inlines = [DetallePedidoInline]

# Configuración del panel de administración para los mensajes enviados desde el formulario de contacto
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    # Campos visibles en la lista de mensajes
    list_display = ('nombre', 'email', 'fecha_creacion')
    
    # Filtro lateral por fecha de creación
    list_filter = ('fecha_creacion',)
    
    # Permite buscar mensajes por nombre, correo electrónico o contenido del mensaje
    search_fields = ('nombre', 'email', 'mensaje')
    
    # Hace que el campo fecha_creacion sea solo lectura (no se puede editar desde el admin)
    readonly_fields = ('fecha_creacion',)
