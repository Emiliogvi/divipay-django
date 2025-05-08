from django.forms import ModelForm
from .models import Grupo
from .models import Gasto
from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'descripcion']

class GastoForm(ModelForm):
    class Meta:
        model = Gasto
        fields = ['grupo', 'nombre', 'monto', 'numero_pagadores']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['grupo'].queryset = Grupo.objects.filter(creador=user)

class usuarioform(UserCreationForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))
    telefono = forms.CharField(required=False)
    direccion = forms.CharField(required=False)
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'bio', 'telefono', 'direccion', 'fecha_nacimiento']