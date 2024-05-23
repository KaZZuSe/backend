from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .custom_manager import UserCustomManager




class Usuario(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    imagen = models.ImageField(upload_to='images_profile/', blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    direccion = models.CharField(max_length=255)
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
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "password","direccion"]
    objects = UserCustomManager()

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='images_producto/', blank=True)
    talla = models.CharField(max_length=2, blank=True)
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
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='producto')	
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario')

class Carrito(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
class CarritoProducto(models.Model):
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Pago(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_pago = models.CharField(default='tarjeta', choices=[
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'Paypal'),
        ('contrarreembolso', 'Contrarreembolso'),
    ])
    num_tarjeta = models.CharField(max_length=16)
    fecha_vencimiento = models.DateField()
    cvc = models.CharField(max_length=3)

class Favorito(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Pedido(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_pedido = models.DateField(auto_now_add=True)
    estado = models.CharField(default='no pagado', choices=[
        ('enviado', 'Enviado'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado'),
        ('no pagado', 'No pagado'),
        ('pagado', 'Pagado'),
    ])
    id_pago = models.ForeignKey(Pago, on_delete=models.CASCADE, null=True, blank=True)

class PedidoProducto(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Venta(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_usuario_comprador = models.ForeignKey(Usuario, related_name='comprador', on_delete=models.CASCADE)
    id_usuario_vendedor = models.ForeignKey(Usuario, related_name='vendedor', on_delete=models.CASCADE)
"""     accion = models.CharField(max_length=255, choices=[
        ('compra', 'Compra'),
        ('venta', 'Venta'),
    ]) """
