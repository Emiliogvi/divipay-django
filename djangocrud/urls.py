"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('create_grupos/', views.create_grupos, name='create_grupos'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('gasto/', views.crear_gasto, name='crear_gasto'),
    path('grupos/', views.grupos, name='grupos'),
    path('detalle_grupo/<int:grupo_id>/', views.detalle_grupo, name='detalle_grupo'),
    path('detalle_grupo/<int:grupo_id>/eliminar', views.eliminar_grupo, name='eliminar_grupo'),
    path('resultadoGasto/<int:gasto_id>/', views.resultado_gasto, name='resultadoGasto'),
    path('historial/', views.historial_gastos, name='historial_gastos'),
    path('gasto/<int:gasto_id>/', views.detalle_gasto, name='detalle_gasto'),

]
