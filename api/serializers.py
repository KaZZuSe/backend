from rest_framework import serializers
from api.models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer(read_only=True, many=True)
    class Meta:
        model = Producto
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer(read_only=True, many=True)
    id_producto = ProductoSerializer(read_only=True, many=True)
    class Meta:
        model = Carrito
        fields = '__all__'

class FavoritoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer(read_only=True, many=True)
    id_producto = ProductoSerializer(read_only=True, many=True)
    class Meta:
        model = Favorito
        fields = '__all__'
class PedidoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer(read_only=True, many=True)
    id_carrito = CarritoSerializer(read_only=True, many=True)
    class Meta:
        model = Pedido
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    id_usuario_comprador = UsuarioSerializer(read_only=True, many=True)
    id_usuario_vendededor = UsuarioSerializer(read_only=True, many=True)
    id_carrito = CarritoSerializer(read_only=True, many=True)
    class Meta:
        model = Venta
        fields = '__all__'