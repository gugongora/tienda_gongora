from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sucursal, Stock, Pedido, MensajeContacto
from .serializers import SucursalSerializer, StockSerializer, PedidoSerializer, MensajeContactoSerializer

# Clase de permiso personalizada que limita el acceso solo a usuarios internos
class SucursalPermission(permissions.BasePermission):
    """
    Permiso personalizado para limitar el acceso a las sucursales solo a usuarios internos
    """
    def has_permission(self, request, view):
        # Permite el acceso solo si el usuario pertenece al grupo 'personal_interno'
        return request.user.groups.filter(name='personal_interno').exists()

# ViewSet de solo lectura para mostrar las sucursales
class SucursalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    # Aplica el permiso personalizado definido arriba
    permission_classes = [SucursalPermission]
    
    # Acción adicional para obtener el stock de una sucursal específica
    @action(detail=True, methods=['get'])
    def stock(self, request, pk=None):
        # Obtiene la sucursal en base al ID en la URL
        sucursal = self.get_object()
        # Filtra el stock correspondiente a esa sucursal
        stocks = Stock.objects.filter(sucursal=sucursal)
        # Serializa y retorna el stock
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

# ViewSet completo (CRUD) para gestionar pedidos
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    # Solo accesible por usuarios internos
    permission_classes = [SucursalPermission]
    
    # Al crear un pedido, puedes asociarlo al usuario autenticado si es necesario
    def perform_create(self, serializer):
        serializer.save()

    # Filtra los pedidos que puede ver un usuario
    def get_queryset(self):
        user = self.request.user
        # Si es superusuario, puede ver todos los pedidos
        if user.is_superuser:
            return Pedido.objects.all()
        # Si no es superusuario, solo puede ver los pedidos de sus sucursales asociadas
        # Se asume que existe una relación: usuario -> sucursales
        return Pedido.objects.filter(sucursal__in=user.sucursales.all())

# ViewSet para gestionar mensajes de contacto desde el sitio (ej. formulario público)
class ContactoViewSet(viewsets.ViewSet):
    # Permite que cualquier persona (incluso no autenticada) pueda usar esta vista
    permission_classes = [permissions.AllowAny]
    
    # Crea un nuevo mensaje de contacto
    def create(self, request):
        # Valida y guarda el mensaje recibido desde el frontend
        serializer = MensajeContactoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Devuelve un mensaje de éxito
        return Response({"mensaje": "Su mensaje ha sido enviado correctamente"}, 
                        status=status.HTTP_201_CREATED)
