from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Formulario personalizado para registrar usuarios, basado en el formulario estándar UserCreationForm de Django
class UserRegisterForm(UserCreationForm):
    # Campo adicional para el email, obligatorio en este formulario
    email = forms.EmailField(required=True)

    class Meta:
        # Modelo en el que se basará el formulario (el modelo User de Django)
        model = User
        # Campos que se mostrarán y solicitarán en el formulario de registro
        fields = ['username', 'email', 'password1', 'password2']
