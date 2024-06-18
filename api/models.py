from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .custom_manager import UserCustomManager

"""
Modelos de la base de datos
Cada modelo representa una tabla de la base de datos

"""
class Usuario(AbstractUser, PermissionsMixin):
    # Definición de los campos adicionales que tendrá el modelo de Usuario.
    username = models.CharField(max_length=255, unique=True)  # Campo de nombre de usuario único.
    email = models.EmailField(max_length=255, unique=True)  # Campo de correo electrónico único.
    imagen = models.ImageField(upload_to='images_profile/', blank=True)  # Imagen de perfil del usuario.
    descripcion = models.CharField(max_length=255, blank=True)  # Descripción o biografía del usuario.
    fecha_creacion = models.DateField(auto_now_add=True)  # Fecha de creación del usuario, se establece automáticamente.
    direccion = models.CharField(max_length=255)  # Dirección del usuario.
    
    # Campos para grupos y permisos personalizados con nombres de campo y consulta personalizados.
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
    
    # Configuración de los campos necesarios para la autenticación.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "password", "direccion"]
    
    # Asignar nuestro administrador de usuarios personalizado.
    objects = UserCustomManager()
class Producto(models.Model):
    # Definición del modelo Producto, que representa un producto en la aplicación.
    nombre = models.CharField(max_length=255)  # Nombre del producto.
    descripcion = models.CharField(max_length=255)  # Descripción del producto.
    
    # Campos para almacenar imágenes del producto.
    imagen = models.ImageField(upload_to='images_producto/', blank=True)
    imagen2 = models.ImageField(upload_to='images_producto/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='images_producto/', blank=True, null=True)
    imagen4 = models.ImageField(upload_to='images_producto/', blank=True, null=True)
    imagen5 = models.ImageField(upload_to='images_producto/', blank=True, null=True)
    
    talla = models.CharField(max_length=2, blank=True)  # Talla del producto.
    
    # Categoría del producto con opciones predefinidas.
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
    
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto.
    vendido = models.BooleanField(default=False)  # Indica si el producto ha sido vendido.
    
    # Relación con el modelo Usuario, indicando quién es el dueño del producto.
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Carrito(models.Model):
    # Definición del modelo Carrito, que representa un carrito de compras.
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario propietario del carrito.
class CarritoProducto(models.Model):
    # Definición del modelo CarritoProducto, que representa la relación entre un carrito y los productos que contiene.
    id_carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)  # Carrito al que pertenece el producto.
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto en el carrito.
class Pago(models.Model):
    # Definición del modelo Pago, que representa un pago realizado por un usuario.
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario que realiza el pago.
    
    # Tipo de pago con opciones predefinidas.
    tipo_pago = models.CharField(default='contrarreembolso', choices=[
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'Paypal'),
        ('contrarreembolso', 'Contrarreembolso'),
    ])
    
    # Campos adicionales para información de tarjeta de crédito.
    num_tarjeta = models.CharField(max_length=16, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    cvc = models.CharField(max_length=3, blank=True, null=True)
    nombre_tarjeta = models.CharField(max_length=255, blank=True, null=True)

class Favorito(models.Model):
    # Definición del modelo Favorito, que representa la relación entre un usuario y sus productos favoritos.
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario que tiene el favorito.
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto marcado como favorito.

# Definición del modelo Pedido, que representa un pedido realizado por un usuario.
class Pedido(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario que realiza el pedido.
    fecha_pedido = models.DateField(auto_now_add=True)  # Fecha de creación del pedido.
    
    # Estado del pedido con opciones predefinidas.
    estado = models.CharField(default='no pagado', choices=[
        ('enviado', 'Enviado'),
        ('recibido', 'Recibido'),
        ('cancelado', 'Cancelado'),
        ('no pagado', 'No pagado'),
        ('pagado', 'Pagado'),
    ])
    direccion = models.CharField(max_length=255, blank=True)  # Dirección de envío del pedido.
    direccion_facturacion = models.CharField(max_length=255, blank=True)  # Dirección de facturación del pedido.
    id_pago = models.ForeignKey(Pago, on_delete=models.CASCADE, null=True, blank=True)  # Pago asociado al pedido.

class PedidoProducto(models.Model):
    # Definición del modelo PedidoProducto, que representa la relación entre un pedido y los productos que contiene.
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Pedido al que pertenece el producto.
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto en el pedido.
class Venta(models.Model):
    # Definición del modelo Venta, que representa una venta de un producto entre usuarios.
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto vendido.
    id_usuario_comprador = models.ForeignKey(Usuario, related_name='comprador', on_delete=models.CASCADE)  # Usuario comprador.
    id_usuario_vendedor = models.ForeignKey(Usuario, related_name='vendedor', on_delete=models.CASCADE)  # Usuario vendedor.