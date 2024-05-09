from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/', UsuarioView.as_view()),
    path('usuarios/<int:pk>/', DetailedUsuarioView.as_view()),
    path('productos/', ProductoView.as_view()),
    path('productos/<int:pk>/', DetailedProductoView.as_view()),
    path('carritos/', CarritoView.as_view()),
    path('carritos/<int:pk>/', DetailedCarritoView.as_view()),
    path('carritos/<int:pk>/productos/', CarritoProductoView.as_view()),
    path('carritos/<int:pk>/productos/<int:pk2>/', CarritoProductoView.as_view()),
    path('favoritos/', FavoritoView.as_view()),
    path('favoritos/<int:pk>/', DetailedFavoritoView.as_view()),
    path('ventas/', VentaView.as_view()),
    path('ventas/<int:pk>/', DetailedVentaView.as_view()),
    path('pedidos/', PedidoView.as_view()),
    path('pedidos/<int:pk>/', DetailedPedidoView.as_view()),
    path('pedidos/<int:pk>/productos/', PedidoProductoView.as_view()),
    path('pedidos/<int:pk>/productos/<int:pk2>/', PedidoProductoView.as_view()),
    path('pagos/', PagoView.as_view()),
    path('pagos/<int:pk>/', DetailedPagoView.as_view()),
]

