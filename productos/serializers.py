
# productos/serializers.py
from rest_framework import serializers
from .models import Producto, Categoria, Marca, Precio

class PrecioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precio
        fields = ['fecha', 'valor']

class ProductoListSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    precio_actual = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'marca_nombre', 'categoria_nombre', 'precio_actual']
    
    def get_precio_actual(self, obj):
        precio = obj.precios.first()
        if precio:
            return precio.valor
        return None

class ProductoDetailSerializer(serializers.ModelSerializer):
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    precios = PrecioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Producto
        fields = ['codigo', 'codigo_fabricante', 'nombre', 'descripcion', 
                 'marca_nombre', 'categoria_nombre', 'precios']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']

class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id', 'nombre']