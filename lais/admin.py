from django.contrib import admin
from .models import cidadao, agendado


class CidadaoAdmin(admin.ModelAdmin):
    ...


class AgendadoAdmin(admin.ModelAdmin):
    ...


admin.site.register(cidadao, CidadaoAdmin)
admin.site.register(agendado, CidadaoAdmin)

# Register your models here.
