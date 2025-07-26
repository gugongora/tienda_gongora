from .forms import UserRegisterForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

def login_register(request):
    login_form = AuthenticationForm()
    register_form = UserRegisterForm()

    if request.method == 'POST':
        # Diferenciar qué formulario se envió
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('store:product_list')  # o donde corresponda
        elif 'register_submit' in request.POST:
            register_form = UserRegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Tu cuenta ha sido creada. Ya puedes iniciar sesión.')
                return redirect('users:login_register')

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'users/login_register.html', context)
