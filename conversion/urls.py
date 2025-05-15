from django.urls import path
from . import views

app_name = 'conversion'

urlpatterns = [
    path("convertir/", views.convertir_moneda, name="convertir_moneda"),
     path("convertir/vista/", views.convertir_moneda_template, name="convertir_moneda_template"),
]
