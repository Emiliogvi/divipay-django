from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Grupo
from .forms import GastoForm
from .models import Gasto
from .models import Usuario
from .forms import usuarioform
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
def historial_gastos(request):
    gastos = Gasto.objects.filter(grupo__creador=request.user).order_by('-fecha')
    return render(request, 'historial_gastos.html', {'gastos': gastos})

@login_required
def crear_gasto(request):
    if request.method == 'GET':
        form = GastoForm(user=request.user)
        return render(request, 'gasto.html', {
            'form': form
        })
    else:
        try:
            form = GastoForm(request.POST, user=request.user)
            nuevo_gasto = form.save(commit=False)
            nuevo_gasto.user = request.user  # Si tu modelo Gasto tiene este campo
            nuevo_gasto.save()
            return redirect('resultadoGasto', gasto_id=nuevo_gasto.id)
        except ValueError:
            form = GastoForm(request.POST, user=request.user)
            return render(request, 'gasto.html', {
                'form': form,
                'error': 'Por favor provee un dato válido'
            })

@login_required
def detalle_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id, grupo__creador=request.user)
    return render(request, 'detalle_gasto.html', {'gasto': gasto})


@login_required
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id, creador=request.user)
    if request.method == 'POST':
        grupo.delete()
        return redirect('grupos')

@login_required    
def detalle_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)  # mover esta línea fuera del if/else para no repetirla

    if request.method == 'GET':
        form = TaskForm(instance=grupo)
        return render(request, 'detalle_grupo.html', {'grupo': grupo, 'form': form})
    else:
        form = TaskForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect('grupos')
        else:
            return render(request, 'detalle_grupo.html', {'grupo': grupo, 'form': form})


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': usuarioform()
        })
    else:
        form = usuarioform(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Crear perfil extendido
                Usuario.objects.create(
                    user=user,
                    bio=form.cleaned_data.get('bio'),
                    telefono=form.cleaned_data.get('telefono'),
                    direccion=form.cleaned_data.get('direccion'),
                    fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento')
                )
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Corrige los errores del formulario'
            })



@login_required
def grupos(request):
    grupos = Grupo.objects.filter(creador=request.user)
    return render(request, 'grupos.html', {'grupos': grupos})

@login_required
def resultado_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id)
    num_pagadores = gasto.numero_pagadores

    if num_pagadores > 0:
        aporte_por_persona = gasto.monto / num_pagadores
    else:
        aporte_por_persona = 0

    return render(request, 'resultadoGasto.html', {
        'gasto': gasto,
        'aporte': round(aporte_por_persona, 2),
        'num_pagadores': num_pagadores
    })

@login_required
def create_grupos(request,):
    if request.method == 'GET' :
        return render(request, 'create_grupos.html', {
            'form' : TaskForm
        })
    else:
        form = TaskForm(request.POST)
        new_grupo = form.save(commit=False)
        new_grupo.creador = request.user
        new_grupo.save()
        print(new_grupo)
        return redirect('grupos')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
        })
        
        else: 
            login(request, user)
            return redirect('home')