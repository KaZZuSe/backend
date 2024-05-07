from django.contrib import admin
from api.models import *

admin.site.register(Usuario)
admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(Pedido)
admin.site.register(Venta)
admin.site.register(Favorito)

# Register your models here.
