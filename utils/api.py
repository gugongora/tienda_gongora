from django.conf import settings

def build_api_url(endpoint):
    """
    Construye la URL completa para consumir la API interna.
    """
    base_url = settings.API_BASE_URL.rstrip('/') + '/'
    return f"{base_url}{endpoint.lstrip('/')}"
