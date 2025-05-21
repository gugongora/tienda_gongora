from django.shortcuts import redirect
from django.urls import resolve

# Middleware personalizado que redirige usuarios según su grupo al intentar acceder a ciertas vistas
class RedirectByGroupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Guarda la función para obtener la respuesta siguiente en la cadena de middleware

    def __call__(self, request):
        # Solo aplica si el usuario está autenticado
        if request.user.is_authenticated:
            # Verifica si el usuario pertenece al grupo 'personal_interno'
            grupo_interno = request.user.groups.filter(name='personal_interno').exists()

            # Obtiene el nombre de la URL actual a partir de la ruta de la solicitud
            path_actual = resolve(request.path_info).url_name

            # Si es personal interno y está en la vista 'product_list', redirige al dashboard interno
            #if grupo_interno and path_actual == 'product_list':
            #  return redirect('store:dashboard_interno')

            # Si no es personal interno y está en el dashboard interno, redirige a la lista de productos
            #elif not grupo_interno and path_actual == 'dashboard_interno':
            #    return redirect('store:product_list')

        # Si no se cumple ninguna condición, sigue con el flujo normal de la petición
        return self.get_response(request)
