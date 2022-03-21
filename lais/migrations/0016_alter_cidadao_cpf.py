# Generated by Django 4.0.3 on 2022-03-21 16:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lais', '0015_alter_agendados_cpf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cidadao',
            name='cpf',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='fk', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]