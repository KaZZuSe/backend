from rest_framework import serializers
from api.models import *
"""

Los serializadores se encargan de convertir los datos de los modelos en formatos JSON.

"""
class UsuarioSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Usuario.
    class Meta:
        model = Usuario
        # Campos que se incluirán en el serializador.
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'imagen', 'descripcion', 'fecha_creacion', 'direccion']
        extra_kwargs = {
            'password': {'write_only': True},  # El campo de contraseña solo será de escritura.
        }

    def update(self, instance, validated_data):
        # Sobrescribe el método update para manejar la actualización de la contraseña correctamente.
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

class ProductoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Producto.
    id_usuario = UsuarioSerializer(read_only=True)  # Usuario propietario del producto, de solo lectura.
    class Meta:
        model = Producto
        fields = '__all__'  # Incluye todos los campos del modelo Producto.

class CarritoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Carrito.
    id_usuario = UsuarioSerializer  # Usuario propietario del carrito.
    class Meta:
        model = Carrito
        fields = '__all__'  # Incluye todos los campos del modelo Carrito.

class CarritoProductoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo CarritoProducto.
    id_carrito = CarritoSerializer  # Carrito al que pertenece el producto.
    id_producto = ProductoSerializer(read_only=True)  # Producto en el carrito, de solo lectura.
    class Meta:
        model = CarritoProducto
        fields = '__all__'  # Incluye todos los campos del modelo CarritoProducto.

class FavoritoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Favorito.
    id_usuario = UsuarioSerializer()  # Usuario que tiene el favorito.
    id_producto = ProductoSerializer(read_only=True)  # Producto marcado como favorito, de solo lectura.
    class Meta:
        model = Favorito
        fields = '__all__'  # Incluye todos los campos del modelo Favorito.

class PagoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Pago.
    id_usuario = UsuarioSerializer  # Usuario que realiza el pago.
    class Meta:
        model = Pago
        fields = '__all__'  # Incluye todos los campos del modelo Pago.

class PedidoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Pedido.
    id_usuario = UsuarioSerializer  # Usuario que realiza el pedido.
    class Meta:
        model = Pedido
        fields = '__all__'  # Incluye todos los campos del modelo Pedido.

class PedidoProductoSerializer(serializers.ModelSerializer):
    # Serializador para el modelo PedidoProducto.
    id_pedido = PedidoSerializer  # Pedido al que pertenece el producto.
    id_producto = ProductoSerializer  # Producto en el pedido.
    class Meta:
        model = PedidoProducto
        fields = '__all__'  # Incluye todos los campos del modelo PedidoProducto.

class PedidoProductoSerializerDialog(serializers.ModelSerializer):
    # Serializador para el modelo PedidoProducto, pero solo lectura para los campos de pedido y producto.
    id_pedido = PedidoSerializer(read_only=True)  # Pedido al que pertenece el producto, de solo lectura.
    id_producto = ProductoSerializer(read_only=True)  # Producto en el pedido, de solo lectura.
    class Meta:
        model = PedidoProducto
        fields = '__all__'  # Incluye todos los campos del modelo PedidoProducto.

class VentaSerializer(serializers.ModelSerializer):
    # Serializador para el modelo Venta.
    id_usuario_comprador = UsuarioSerializer  # Usuario que compra el producto.
    id_usuario_vendedor = UsuarioSerializer  # Usuario que vende el producto.
    class Meta:
        model = Venta
        fields = '__all__'  # Incluye todos los campos del modelo Venta.
