from django.db import models

# Create your models here.
from django.db import models


class unidade(models.Model):
    cod_und = models.IntegerField(primary_key=True)
    nome_und = models.CharField(max_length=300)
