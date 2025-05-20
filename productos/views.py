from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Producto, Categoria, Marca
from .serializers import ProductoListSerializer, ProductoDetailSerializer, CategoriaSerializer, MarcaSerializer

# ViewSet solo de lectura para el modelo Producto
class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    # Define el conjunto de datos base a consultar (todos los productos)
    queryset = Producto.objects.all()

    # Método para usar diferentes serializadores según la acción
    def get_serializer_class(self):
        # Si se está recuperando el detalle de un solo producto, usar el serializador detallado
        if self.action == 'retrieve':
            return ProductoDetailSerializer
        # Para el resto de los casos (como list), usar el serializador resumido
        return ProductoListSerializer

    # Define los permisos: cualquier persona puede acceder (sin autenticación)
    def get_permissions(self):
        return [permissions.AllowAny()]

    # Permite filtrar productos por ID de categoría o ID de marca usando parámetros en la URL
    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria_id = self.request.query_params.get('categoria')  # ?categoria=1
        marca_id = self.request.query_params.get('marca')  # ?marca=2

        # Filtra por categoría si se proporciona
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        # Filtra por marca si se proporciona
        if marca_id:
            queryset = queryset.filter(marca_id=marca_id)

        return queryset

    # Método adicional para obtener productos por categoría usando un parámetro explícito
    # (Este método necesita decorarse con @action si se quiere usar en rutas automáticas)
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria_id')
        if categoria_id:
            productos = Producto.objects.filter(categoria_id=categoria_id)
            serializer = self.get_serializer(productos, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar una categoría"}, status=400)

# ViewSet solo de lectura para mostrar las categorías disponibles
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    # Permite acceso sin autenticación
    permission_classes = [permissions.AllowAny]

# ViewSet solo de lectura para mostrar las marcas disponibles
class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    # Permite acceso sin autenticación
    permission_classes = [permissions.AllowAny]
