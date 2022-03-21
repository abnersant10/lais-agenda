# Generated by Django 4.0.3 on 2022-03-21 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lais', '0013_rename_unidade_agendados'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendados',
            name='cpf',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='fk_ag', serialize=False, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='agendados',
            name='cod_und',
            field=models.IntegerField(),
        ),
    ]