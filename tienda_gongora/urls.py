"""
Configuración de URLs para el proyecto tienda_gongora.

La lista `urlpatterns` dirige las URLs hacia las vistas correspondientes.
"""

from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

# Router para vistas con ViewSets de Django REST Framework (DRF)
from rest_framework.routers import DefaultRouter
from rest_framework import permissions

# Para la documentación Swagger y Redoc (generación automática de documentación API)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Para redirecciones de URLs
from django.urls import reverse_lazy
from django.views.generic import RedirectView

# Autenticación con JWT (tokens para autenticación segura en la API)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Importación de los ViewSets personalizados que manejan los datos y lógica de la API
from productos.views import ProductoViewSet, CategoriaViewSet, MarcaViewSet
from operaciones.views import SucursalViewSet, PedidoViewSet, ContactoViewSet

# Configuración de la vista de esquema/documentación de la API con datos como título, versión, contacto, etc.
schema_view = get_schema_view(
   openapi.Info(
      title="Tienda Góngora API",              # Nombre de la API para la documentación
      default_version='v1',                      # Versión actual de la API
      description="API para la gestión de productos y pedidos de Tienda Góngora",  # Descripción breve
      terms_of_service="https://www.tiendagongora.com/terms/",  # Términos de uso
      contact=openapi.Contact(email="contact@tiendagongora.com"),  # Contacto para soporte
      license=openapi.License(name="Privada"),   # Licencia de uso
   ),
   public=True,                                   # Documentación pública
   permission_classes=(permissions.AllowAny,),   # Permite acceso a cualquier usuario
)

# Crear un enrutador automático para los ViewSets, así se generan las rutas REST automáticamente
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)       # Rutas para manejar productos (ejemplo: /api/productos/)
router.register(r'categorias', CategoriaViewSet)     # Rutas para categorías de productos
router.register(r'marcas', MarcaViewSet)             # Rutas para marcas de productos
router.register(r'sucursales', SucursalViewSet)      # Rutas para sucursales
router.register(r'pedidos', PedidoViewSet)           # Rutas para pedidos

urlpatterns = [
    # Redirecciona la raíz del sitio web hacia el listado de productos de la tienda (página principal)
    path('', RedirectView.as_view(url=reverse_lazy('store:product_list'), permanent=False)),
    
    # Ruta para el panel administrativo de Django
    path('admin/', admin.site.urls),

    # Incluir URLs de aplicaciones específicas del proyecto
    path('cart/', include('cart.urls')),                   # Rutas para el carrito de compras
    path('orders/', include('orders.urls')),               # Rutas para las órdenes de compra
    path('users/', include(('users.urls', 'users'), namespace='users')),  # Gestión de usuarios (login, registro, etc.)
    path('webpay/', include('payments.urls')),             # Integración con el sistema de pago WebPay
    path('conversion/', include('conversion.urls')),       # Rutas para conversión de monedas o datos
    path('store/', include(('store.urls', 'store'), namespace='store')),  # URLs principales de la tienda web

    # Incluir las rutas generadas automáticamente por el router para la API REST
    path('api/', include(router.urls)),

    # Ruta para contacto, aquí se maneja con un ViewSet básico, no con ViewSet estándar de DRF
    path('api/contacto/', ContactoViewSet.as_view({'post': 'create'}), name='contacto'),

    # Redirecciona /dashboard/ hacia el dashboard principal de la tienda (interfaz administrativa)
    path('dashboard/', RedirectView.as_view(url='/store/dashboard/', permanent=True), name='dashboard_redirect'),

    # Autenticación para la API REST usando JWT
    path('api-auth/', include('rest_framework.urls')),  # Login y logout para el API Browsable (interfaz web de DRF)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),       # Obtener token JWT (login)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      # Refrescar token JWT

    # Rutas para la documentación de la API generada automáticamente con Swagger y Redoc
    re_path(r'^swagger(?P<format>json|yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # JSON/YAML de la documentación
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Interfaz Swagger UI (interactiva)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),            # Interfaz Redoc para documentación más simple
]

# Durante desarrollo, servir archivos multimedia (imágenes, archivos subidos) directamente desde MEDIA_URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
