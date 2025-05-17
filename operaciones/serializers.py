# operaciones/serializers.py
from rest_framework import serializers
from .models import Sucursal, Stock, Pedido, DetallePedido, MensajeContacto
from productos.models import Producto

class StockSerializer(serializers.ModelSerializer):
    producto_codigo = serializers.ReadOnlyField(source='producto.codigo')
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = Stock
        fields = ['producto_codigo', 'producto_nombre', 'cantidad']

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_codigo = serializers.PrimaryKeyRelatedField(
        source='producto', queryset=Producto.objects.all()
    )
    
    class Meta:
        model = DetallePedido
        fields = ['producto_codigo', 'cantidad']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True)
    sucursal_id = serializers.PrimaryKeyRelatedField(
        source='sucursal', queryset=Sucursal.objects.all()
    )
    
    class Meta:
        model = Pedido
        fields = ['id', 'sucursal_id', 'fecha_creacion', 'estado', 'notas', 'detalles']
    
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        pedido = Pedido.objects.create(**validated_data)
        
        for detalle_data in detalles_data:
            DetallePedido.objects.create(pedido=pedido, **detalle_data)
        
        return pedido

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'telefono']

class MensajeContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'telefono', 'mensaje']