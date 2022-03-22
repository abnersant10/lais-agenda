"""agend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from lais.views import home, cadastro, pag_inicial, logout_view, agendamento, listagem

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cadastro', cadastro, name='cadastro'),
    path('pag_inicial', pag_inicial, name='pag_inicial'),
    path('logout', logout_view, name="logout"),
    path('agendamento', agendamento, name='agendamento'),
    path('listagem', listagem, name='listagem'),
]
