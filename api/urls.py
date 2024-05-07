from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/', UsuarioView.as_view()),
    path('productos/', ProductoView.as_view()),
    path('carritos/', CarritoView.as_view()),
    path('favoritos/', FavoritoView.as_view()),
    path('ventas/', VentaView.as_view()),
    path('pedidos/', PedidoView.as_view()),
]

