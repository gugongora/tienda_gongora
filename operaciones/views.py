# operaciones/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sucursal, Stock, Pedido, MensajeContacto
from .serializers import SucursalSerializer, StockSerializer, PedidoSerializer, MensajeContactoSerializer

class SucursalPermission(permissions.BasePermission):
    """
    Permiso personalizado para limitar el acceso a las sucursales solo a usuarios internos
    """
    def has_permission(self, request, view):
        # Aquí implementa la lógica para identificar usuarios internos
        # Por ejemplo, verificar si pertenecen a un grupo específico
        return request.user.groups.filter(name='personal_interno').exists()

class SucursalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    permission_classes = [SucursalPermission]
    
    @action(detail=True, methods=['get'])
    def stock(self, request, pk=None):
        sucursal = self.get_object()
        stocks = Stock.objects.filter(sucursal=sucursal)
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [SucursalPermission]
    
    def perform_create(self, serializer):
        # Asocia el pedido con el usuario actual (asumiendo que cada usuario está vinculado a una sucursal)
        serializer.save()
    
    def get_queryset(self):
        # Filtra pedidos por la sucursal del usuario
        user = self.request.user
        if user.is_superuser:
            return Pedido.objects.all()
        # Asumiendo que tienes una relación entre usuario y sucursal
        return Pedido.objects.filter(sucursal__in=user.sucursales.all())

class ContactoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serializer = MensajeContactoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"mensaje": "Su mensaje ha sido enviado correctamente"}, 
                       status=status.HTTP_201_CREATED)