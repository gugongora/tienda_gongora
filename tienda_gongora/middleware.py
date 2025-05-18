from django.shortcuts import redirect
from django.urls import resolve

class RedirectByGroupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            grupo_interno = request.user.groups.filter(name='personal_interno').exists()  # ← corregido
            path_actual = resolve(request.path_info).url_name

            if grupo_interno and path_actual == 'product_list':
                return redirect('store:dashboard_interno')
            elif not grupo_interno and path_actual == 'dashboard_interno':
                return redirect('store:product_list')

        return self.get_response(request)
