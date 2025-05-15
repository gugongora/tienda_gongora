from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pagar/', views.iniciar_pago, name='webpay_pagar'),
    path('confirmacion/', views.webpay_confirmacion, name='webpay_confirmacion'),
]