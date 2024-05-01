from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    imagen = models.CharField(max_length=255, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_user_permissions",
        related_query_name="user",
    )

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    imagen = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255, choices=[
        ('pantalon', 'Pantalón'),
        ('camiseta', 'Camiseta'),
        ('sudadera', 'Sudadera'),
        ('chaqueta', 'Chaqueta'),
        ('cazadora', 'Cazadora'),
        ('zapato', 'Zapato'),
        ('zapatilla', 'Zapatilla'),
        ('accesorio', 'Accesorio'),
        ('bermuda', 'Bermuda'),
    ])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Carrito(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Favorito(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Pago(models.Model):
    estado = models.CharField(max_length=255, choices=[
        ('pagado', 'Pagado'),
        ('no pagado', 'No pagado'),
    ])
    tipo = models.CharField(max_length=255, choices=[
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'Paypal'),
        ('contrareembolso', 'Contrareembolso'),
    ])

class Pedido(models.Model):
    id_pago = models.ForeignKey(Pago, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Venta(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_usuario_comprador = models.ForeignKey(Usuario, related_name='comprador', on_delete=models.CASCADE)
    id_usuario_vendedor = models.ForeignKey(Usuario, related_name='vendedor', on_delete=models.CASCADE)
    accion = models.CharField(max_length=255, choices=[
        ('compra', 'Compra'),
        ('venta', 'Venta'),
    ])
