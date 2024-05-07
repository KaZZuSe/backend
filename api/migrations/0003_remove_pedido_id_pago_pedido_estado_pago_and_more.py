# Generated by Django 5.0.4 on 2024-05-07 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_carrito_favorito_pago_pedido_producto_usuario_venta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='id_pago',
        ),
        migrations.AddField(
            model_name='pedido',
            name='estado_pago',
            field=models.CharField(choices=[('pagado', 'Pagado'), ('no pagado', 'No pagado')], default='no pagado'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='tipo_pago',
            field=models.CharField(choices=[('tarjeta', 'Tarjeta'), ('paypal', 'Paypal'), ('contrarreembolso', 'Contrarreembolso')], default='tarjeta'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='images_producto/'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(blank=True, upload_to='images_profile/'),
        ),
        migrations.DeleteModel(
            name='Pago',
        ),
    ]
