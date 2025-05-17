from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('productos/', views.product_list, name='product_list'),
     path('logout/', LogoutView.as_view(next_page='users:login'), name='logout'),
]   