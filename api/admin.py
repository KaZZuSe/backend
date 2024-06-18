from django.contrib import admin
from api.models import *

"""	
Configurar el administrador para este proyecto.

"""
admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
admin.site.register(Pedido)
admin.site.register(PedidoProducto)
admin.site.register(Venta)
admin.site.register(Favorito)
admin.site.register(Pago)