"""
Configuración de pytest para Django
"""
import os
import django
from django.conf import settings

# Configurar Django para pytest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_gongora.settings')
django.setup() 