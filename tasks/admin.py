from django.contrib import admin
from .models import Grupo, Gasto, Participante, DistribucionGasto

# Register your models here.
admin.site.register(Grupo)
admin.site.register(Gasto)
admin.site.register(Participante)
admin.site.register(DistribucionGasto)