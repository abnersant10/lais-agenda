# Generated by Django 4.0.3 on 2022-03-18 23:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lais', '0002_alter_unidade_cod_und'),
    ]

    operations = [
        migrations.CreateModel(
            name='cidadao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=11, verbose_name='cpf')),
                ('nasc', models.DateField(verbose_name='nasc')),
                ('grp_atend', models.CharField(max_length=100, verbose_name='grp_atend')),
                ('teve_covid', models.CharField(max_length=3, verbose_name='teve_covid')),
                ('senha', models.CharField(max_length=12, verbose_name='senha')),
                ('nome', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]