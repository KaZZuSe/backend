from rest_framework import serializers
from api.models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'imagen', 'descripcion', 'fecha_creacion', 'direccion']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class ProductoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer(read_only=True)
    class Meta:
        model = Producto
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer
    class Meta:
        model = Carrito
        fields = '__all__'
class CarritoProductoSerializer(serializers.ModelSerializer):
    id_carrito = CarritoSerializer
    id_producto = ProductoSerializer(read_only=True)
    class Meta:
        model = CarritoProducto
        fields = '__all__'
class FavoritoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer()
    id_producto = ProductoSerializer(read_only=True)
    class Meta:
        model = Favorito
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer
    class Meta:
        model = Pago
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    id_usuario = UsuarioSerializer
    class Meta:
        model = Pedido
        fields = '__all__'

class PedidoProductoSerializer(serializers.ModelSerializer):
    id_pedido = PedidoSerializer
    id_producto = ProductoSerializer
    class Meta:
        model = PedidoProducto
        fields = '__all__'

class PedidoProductoSerializerDialog(serializers.ModelSerializer):
    id_pedido = PedidoSerializer(read_only=True)
    id_producto = ProductoSerializer(read_only=True)
    class Meta:
        model = PedidoProducto
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    id_usuario_comprador = UsuarioSerializer
    id_usuario_vendedor = UsuarioSerializer
    class Meta:
        model = Venta
        fields = '__all__'