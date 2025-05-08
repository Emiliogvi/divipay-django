from django.db import models
from django.contrib.auth.models import User

# Extiende el modelo de usuario existente mediante un perfil adicional
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Grupo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre + " - by " + self.creador.username

class Gasto(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    monto = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)
    numero_pagadores = models.PositiveIntegerField(default=1, verbose_name="Número de pagadores")


    def __str__(self):
        return self.nombre


class Participante(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    ROLES = (
        ('Administrador', 'Administrador'),
        ('Miembro', 'Miembro')
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='Miembro')

    def __str__(self):
        return self.usuario.username + " fue añadido a un grupo"

class DistribucionGasto(models.Model):
    gasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    monto = models.FloatField()
