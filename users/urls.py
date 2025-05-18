from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page='store:product_list'), name='logout'),
    path('register/', views.register, name='register'),
    
]