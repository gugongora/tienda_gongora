from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='view_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-all/<int:product_id>/', views.remove_all_from_cart, name='remove_all_from_cart'),
    path('increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),

]
