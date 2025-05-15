from django.urls import path
from .views import clp_to_usd_view

app_name = 'conversion'

urlpatterns = [
    path('convert/clp-usd/', clp_to_usd_view, name='clp_to_usd'),
]