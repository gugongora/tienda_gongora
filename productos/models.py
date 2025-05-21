from django.db import models

# Modelo que representa una categoría de productos
class Categoria(models.Model):
    # Nombre de la categoría (máximo 100 caracteres)
    nombre = models.CharField(max_length=100)
    
    # Descripción de la categoría (opcional)
    descripcion = models.TextField(blank=True)
    
    # Representación legible del objeto (para el admin, consola, etc.)
    def __str__(self):
        return self.nombre

# Modelo que representa una marca de productos
class Marca(models.Model):
    # Nombre de la marca (máximo 100 caracteres)
    nombre = models.CharField(max_length=100)
    
    # Representación legible del objeto
    def __str__(self):
        return self.nombre

# Modelo que representa un producto
class Producto(models.Model):
    # ID automático como clave primaria
    id = models.AutoField(primary_key=True)

    # Código único del producto (pero ya no es primary key)
    codigo = models.CharField(max_length=50, unique=True)
    
    # Código del fabricante (puede no ser único)
    codigo_fabricante = models.CharField(max_length=50)
    
    # Nombre del producto (máximo 200 caracteres)
    nombre = models.CharField(max_length=200)
    
    # Descripción del producto (opcional)
    descripcion = models.TextField(blank=True)
    
    # Relación con la marca
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    
    # Relación con la categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    
    # Fecha de creación
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
# Modelo que representa el historial de precios de un producto
class Precio(models.Model):
    # Relación con el producto al que pertenece este precio
    producto = models.ForeignKey(Producto, related_name='precios', on_delete=models.CASCADE)
    
    # Fecha en que se registra el precio (se asigna automáticamente)
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Valor del precio (máximo 12 dígitos, 2 decimales)
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        # Se ordenarán los precios del más reciente al más antiguo por defecto
        ordering = ['-fecha']
