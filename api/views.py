from api.models import *
from api.serializers import *
from rest_framework import status, generics

class UsuarioView(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
class DetailedUsuarioView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProductoView(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class DetailedProductoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class CarritoView(generics.ListCreateAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class DetailedCarritoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class FavoritoView(generics.ListCreateAPIView):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer

class DetailedFavoritoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer

class VentaView(generics.ListCreateAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class DetailedVentaView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class PagoView(generics.ListCreateAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
class DetailedPagoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class PedidoView(generics.ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

class DetailedPedidoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
class PedidoProductoView(generics.ListCreateAPIView):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer

class DetailedPedidoProductoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PedidoProducto.objects.all()
    serializer_class = PedidoProductoSerializer
class CarritoProductoView(generics.ListCreateAPIView):
    queryset = CarritoProducto.objects.all()
    serializer_class = CarritoProductoSerializer

class DetailedCarritoProductoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CarritoProducto.objects.all()
    serializer_class = CarritoProductoSerializer
