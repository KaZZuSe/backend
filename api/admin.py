from django.contrib import admin
from api.models import *

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
admin.site.register(Pedido)
admin.site.register(PedidoProducto)
admin.site.register(Venta)
admin.site.register(Favorito)
admin.site.register(Pago)