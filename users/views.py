from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            # Si el usuario está en personal_interno → dashboard_interno
            if user.groups.filter(name='personal_interno').exists():
                return redirect('store:dashboard_interno')  # Redirección a dashboard_interno
            
            # Si no, a product_list (otros usuarios)
            else:
                return redirect('store:product_list')
        
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Aquí podrías añadir al usuario a un grupo específico si lo necesitas
            # group = Group.objects.get(name='nombre_del_grupo')
            # user.groups.add(group)
            messages.success(request, 'Tu cuenta ha sido creada. Ahora puedes iniciar sesión.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})