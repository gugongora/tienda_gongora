# store/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'store'

urlpatterns = [
    # Ruta principal que muestra la lista de productos
    path('', views.product_list, name='product_list_home'),
    
    # Detalle de producto
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    
    # Búsqueda
    path('search/', views.search, name='search'),
    
    # URL alternativa para productos (mantiene el mismo nombre para consistencia)
    path('productos/', views.product_list, name='product_list'),
    
    # Cierre de sesión
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    
    # Dashboard interno
    path('dashboard/', views.dashboard_interno, name='dashboard_interno'),
]