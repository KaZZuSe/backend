# Generated by Django 5.0.4 on 2024-05-15 11:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_pedido_fecha_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateField(default=datetime.datetime(2024, 5, 15, 11, 33, 55, 387400, tzinfo=datetime.timezone.utc)),
        ),
    ]