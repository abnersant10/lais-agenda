

# Create your models here.
from tkinter.tix import Tree
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class agendado(models.Model):
    cod_und = models.IntegerField()
    nome_und = models.CharField(max_length=300)
    cpf = models.IntegerField(primary_key=True)
    ag_data = models.DateField()

    def __str__(self):
        return self.cpf


class cidadao(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, primary_key=True, related_name='fk')
    nasc = models.DateField(
        "nasc", auto_now=False, auto_now_add=False)
    grp_atend = models.CharField("grp_atend", max_length=100)
    teve_covid = models.CharField("teve_covid", max_length=3)
    senha = models.CharField("senha", max_length=12)

    def __str__(self):
        return self.nome
