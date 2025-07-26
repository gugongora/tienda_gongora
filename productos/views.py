from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Producto, Categoria, Marca
from rest_framework import filters
from .serializers import (
    ProductoListSerializer,
    ProductoDetailSerializer,
    CategoriaSerializer,
    MarcaSerializer
)


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all().order_by('id')
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'descripcion', 'codigo']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductoDetailSerializer
        return ProductoListSerializer

    def get_permissions(self):
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.query_params.get('categoria')
        marca_id = self.request.query_params.get('marca')

        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
        if marca_id:
            queryset = queryset.filter(marca_id=marca_id)

        return queryset

    def get_serializer_context(self):
        return {'request': self.request}  # 👈 NECESARIO para imagen_url

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all().order_by('id')
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.AllowAny]

class MarcaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Marca.objects.all().order_by('id')
    serializer_class = MarcaSerializer
    permission_classes = [permissions.AllowAny]
