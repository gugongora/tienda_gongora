from django.db import models
from productos.models import Producto  # Se importa el modelo Producto desde otra app del proyecto

# Modelo que representa una sucursal física
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)        # Nombre de la sucursal
    direccion = models.CharField(max_length=200)     # Dirección de la sucursal
    telefono = models.CharField(max_length=20)       # Teléfono de contacto
    
    def __str__(self):
        return self.nombre  # Representación legible de la sucursal

# Modelo que representa el stock de productos en una sucursal específica
class Stock(models.Model):
    sucursal = models.ForeignKey(Sucursal, related_name='stocks', on_delete=models.CASCADE)  # Sucursal a la que pertenece el stock
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)                         # Producto del que se tiene stock
    cantidad = models.IntegerField(default=0)                                                # Cantidad de unidades disponibles

    class Meta:
        # Se asegura de que no haya duplicados de producto por sucursal
        unique_together = ('sucursal', 'producto')

# Modelo que representa un pedido de productos realizado por una sucursal
class Pedido(models.Model):
    # Opciones de estado del pedido
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('enviado', 'Enviado'),
        ('recibido', 'Recibido'),
    )
    
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)  # Sucursal que realiza el pedido
    fecha_creacion = models.DateTimeField(auto_now_add=True)          # Fecha en la que se creó el pedido (automática)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')  # Estado del pedido
    notas = models.TextField(blank=True)                              # Notas o comentarios adicionales sobre el pedido
    
    def __str__(self):
        return f"Pedido {self.id} - {self.sucursal.nombre}"  # Representación legible del pedido

# Modelo que representa los detalles (productos y cantidades) dentro de un pedido
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)  # Pedido al que pertenece este detalle
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)                      # Producto solicitado
    cantidad = models.IntegerField()                                                      # Cantidad solicitada del producto
    
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"  # Ejemplo: "3 x Laptop"

# Modelo para mensajes enviados por usuarios desde un formulario de contacto
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)             # Nombre del remitente
    email = models.EmailField()                           # Correo electrónico del remitente
    telefono = models.CharField(max_length=20, blank=True)  # Teléfono (opcional)
    mensaje = models.TextField()                          # Contenido del mensaje
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de envío del mensaje (automática)
    
    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.fecha_creacion})"  # Ejemplo: "Mensaje de Ana (2025-05-20 15:00)"
