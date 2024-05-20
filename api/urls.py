from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('logout/', logout),
    path('usuarios/', UsuarioView.as_view()),
    path('usuarios-detalle/', DetailedUsuarioView.as_view()),
    path('productos/', ProductoView.as_view()),
    path('productos/<int:pk>/', DetailedProductoView.as_view()),
    path('carritos/', CarritoView.as_view()),
    path('carritos/<int:pk>/', DetailedCarritoView.as_view()),
    path('carritos/<int:pk>/productos/', CarritoProductoView.as_view()),
    path('carritos/<int:pk>/productos/<int:product_pk>/', DetailedCarritoProductoView.as_view()),  # pk2 renombrado a product_pk
    path('favoritos/', FavoritoView.as_view()),
    path('favoritos/<int:pk>/', DetailedFavoritoView.as_view()),
    path('favoritos/<int:product_id>/add/', add_favorito),
    path('ventas/', VentaView.as_view()),
    path('ventas/<int:pk>/', DetailedVentaView.as_view()),
    path('pedidos/', PedidoView.as_view()),
    path('pedidos/<int:pk>/', DetailedPedidoView.as_view()),
    path('pedidos/<int:pk>/productos/', PedidoProductoView.as_view()),
    path('pedidos/<int:pk>/productos/<int:product_pk>/', DetailedPedidoProductoView.as_view()),  # pk2 renombrado a product_pk
    path('pedidos/<int:pk>/estado/', update_pedido_status),
    path('pagos/', PagoView.as_view()),
    path('pagos/<int:pk>/', DetailedPagoView.as_view()),
    path('pagos/process/', process_payment),
    path('carrito/add/<int:producto_id>/', add_cart),  # Añadido el endpoint para añadir productos al carrito
    path('carrito/productos/', get_carrito_productos),  # Añadido el endpoint para obtener productos del carrito
    path('favoritos-get', get_favoritos),  # Añadido el endpoint para obtener favoritos
]
