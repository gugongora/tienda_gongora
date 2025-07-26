from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('confirmacion/', views.webpay_confirmacion, name='webpay_confirmacion'),
]