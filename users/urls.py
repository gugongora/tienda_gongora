from django.urls import path
from . import views  # Importa las vistas definidas en este módulo
from django.contrib.auth.views import LogoutView  # Vista genérica para el cierre de sesión
from django.contrib.auth import views as auth_views
app_name = 'users'  # Namespace para las URLs de esta app, para referenciarlas fácilmente en templates y views

urlpatterns = [
    # URL para la página de inicio de sesión, llama a la vista 'login' en views.py
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    # URL para cerrar sesión, usa la vista genérica LogoutView de Django
    # Al cerrar sesión, redirige a la lista de productos de la tienda ('store:product_list')
    path('logout/', LogoutView.as_view(next_page='store:product_list'), name='logout'),

    # URL para la página de registro de nuevos usuarios, llama a la vista 'register' en views.py
    path('register/', views.register, name='register'),
]
