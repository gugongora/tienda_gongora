from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

def login(request):
    # Vista para manejar el inicio de sesión de usuarios
    if request.method == 'POST':
        # Si el formulario fue enviado, crea una instancia de AuthenticationForm con los datos recibidos
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():  # Valida que los datos sean correctos
            user = form.get_user()  # Obtiene el usuario autenticado
            auth_login(request, user)  # Inicia sesión del usuario

            # Verifica si el usuario pertenece al grupo 'personal_interno'
            if user.groups.filter(name='personal_interno').exists():
                # Si es del grupo 'personal_interno', redirige a su dashboard interno
                return redirect('store:dashboard_interno')
            else:
                # Si no, redirige al listado de productos para usuarios normales
                return redirect('store:product_list')
        else:
            # Si el formulario no es válido, muestra un mensaje de error
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        # Si el método no es POST, se muestra un formulario vacío para iniciar sesión
        form = AuthenticationForm()

    # Renderiza la plantilla login.html con el formulario
    return render(request, 'users/login.html', {'form': form})


def register(request):
    # Vista para manejar el registro de nuevos usuarios
    if request.method == 'POST':
        # Si se envió el formulario, crea una instancia con los datos recibidos
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # Valida que los datos sean correctos
            user = form.save()  # Guarda el nuevo usuario en la base de datos

            # Aquí puedes asignar al usuario a un grupo si es necesario (opcional)
            # group = Group.objects.get(name='nombre_del_grupo')
            # user.groups.add(group)

            # Muestra mensaje de éxito indicando que la cuenta fue creada
            messages.success(request, 'Tu cuenta ha sido creada. Ahora puedes iniciar sesión.')
            
            # Redirige a la página de login para que el usuario inicie sesión
            return redirect('users:login')
    else:
        # Si el método no es POST, muestra un formulario vacío para registrarse
        form = UserRegisterForm()

    # Renderiza la plantilla register.html con el formulario
    return render(request, 'users/register.html', {'form': form})
