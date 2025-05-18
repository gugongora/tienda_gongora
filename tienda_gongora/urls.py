"""
URL configuration for tienda_gongora project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path,  re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Importa las vistas que has creado
from productos.views import ProductoViewSet, CategoriaViewSet, MarcaViewSet
from operaciones.views import SucursalViewSet, PedidoViewSet, ContactoViewSet
# Configura la documentación automática
from django.views.generic import RedirectView
schema_view = get_schema_view(
   openapi.Info(
      title="Tienda Góngora API",
      default_version='v1',
      description="API para la gestión de productos y pedidos de Tienda Góngora",
      terms_of_service="https://www.tiendagongora.com/terms/",
      contact=openapi.Contact(email="contact@tiendagongora.com"),
      license=openapi.License(name="Privada"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
# Configura el router para las vistas basadas en viewsets
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'sucursales', SucursalViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('store:product_list'), permanent=False)),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('users/', include(('users.urls', 'users'), namespace='users')),  # solo si tienes users también
    path('webpay/', include('payments.urls')),
    path('conversion/', include('conversion.urls')),
    path('store/', include(('store.urls', 'store'), namespace='store')),
    # URLs para la API
    path('api/', include(router.urls)),
    path('api/contacto/', ContactoViewSet.as_view({'post': 'create'}), name='contacto'),
     path('dashboard/', RedirectView.as_view(url='/store/dashboard/', permanent=True), name='dashboard_redirect'),
    # URLs para autenticación
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # URLs para documentación
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Incluye aquí cualquier otra URL que ya tengas en tu proyecto
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)