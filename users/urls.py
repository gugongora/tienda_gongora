from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    # Vista combinada de login + registro
    path('login/', views.login_register, name='login_register'),

    # Cierre de sesión
    path('logout/', LogoutView.as_view(next_page='store:product_list'), name='logout'),
]
