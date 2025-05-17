from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Producto, Categoria, Marca
from .serializers import ProductoListSerializer, ProductoDetailSerializer, CategoriaSerializer, MarcaSerializer

class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductoDetailSerializer
        return ProductoListSerializer
    
    def get_permissions(self):
        # Para GET /productos y GET /productos/{codigo} permitimos acceso público
        return [permissions.AllowAny()]
    
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria_id')
        if categoria_id:
            productos = Producto.objects.filter(categoria_id=categoria_id)
            serializer = self.get_serializer(productos, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe especificar una categoría"}, status=400)

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]

class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [permissions.AllowAny]