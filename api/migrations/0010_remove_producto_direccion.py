# Generated by Django 5.0.6 on 2024-06-06 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_producto_direccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='direccion',
        ),
    ]