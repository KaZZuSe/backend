# Generated by Django 5.0.6 on 2024-05-23 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_pedido_fecha_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='talla',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
