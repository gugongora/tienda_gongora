from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
