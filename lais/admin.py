from django.contrib import admin
from .models import cidadao


class CidadaoAdmin(admin.ModelAdmin):
    ...


admin.site.register(cidadao, CidadaoAdmin)

# Register your models here.
