# Generated by Django 5.0.4 on 2024-05-14 09:22

import django.contrib.auth.models
import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_carrito_id_producto_remove_carrito_total_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
                ('object', django.db.models.manager.Manager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]