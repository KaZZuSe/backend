# Generated by Django 5.0.6 on 2024-05-23 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_producto_usuario_alter_producto_id_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='usuario',
        ),
    ]
