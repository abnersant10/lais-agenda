from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class unidade(models.Model):
    cod_und = models.IntegerField(primary_key=True)
    nome_und = models.CharField(max_length=300)

# ENTIDADE USUÁRIO


class usuario(models.Model):
    nome = models.CharField("nome", max_length=100)
    cpf = models.CharField("cpf", max_length=11)
    nasc = models.DateField(
        "nasc", auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    grp_atend = models.CharField("grp_atend", max_length=100)
    teve_covid = models.CharField("teve_covid", max_length=3)
    senha = models.CharField("senha", max_length=12)
