# store/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'store'

urlpatterns = [
    # Rutas más específicas primero
    path('productos/', views.product_list, name='product_list'),
    path('producto/<int:product_id>/', views.product_detail, name='product_detail'),  # 🔧 Modificada
    path('search/', views.search, name='search'),
    path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
    path('dashboard/', views.dashboard_interno, name='dashboard_interno'),

    # Ruta base al final
    path('', views.product_list, name='product_list_home'),
]
