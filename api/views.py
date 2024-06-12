from api.models import *
from api.serializers import *
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db.models import Sum, Q
from rest_framework.exceptions import NotFound
from rest_framework.filters import SearchFilter
import time
class UsuarioView(generics.ListCreateAPIView):
    serializer_class = UsuarioSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Usuario.objects.all()
        else:
            return [self.request.user]
        
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_info(request, user_id):
    try:
        usuario = Usuario.objects.get(id=user_id)
        data = {
            'id': usuario.id,
            'username': usuario.username,
            'fecha_creacion': usuario.fecha_creacion,
            'imagen': usuario.imagen.url if usuario.imagen else None,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
class DetailedUsuarioView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            request.data.pop('password')
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            request.data.pop('password')
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        token = request.auth
        if token:
            token.delete()
        return super().delete(request, *args, **kwargs)

@api_view(['POST'])
def register(request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = Usuario.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
    user = get_object_or_404(Usuario, username=request.data.get('username'))
    if not user.check_password(request.data.get('password')):
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)
    return Response({'token': token.key,'user': serializer.data}, status=status.HTTP_200_OK)
@api_view(['GET'])
def logout(request):
    token = request.auth
    if token:
        token.delete()
    return Response(status=status.HTTP_200_OK)
class ProductoView(generics.ListCreateAPIView):
    serializer_class = ProductoSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Producto.objects.filter(~Q(id_usuario=self.request.user.id), vendido=False)
        else:
            queryset = Producto.objects.filter(vendido=False)
        return queryset

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_usuario(request):
    try:
        usuario = Usuario.objects.get(id=request.user.id)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_usuario(request):
    try:
        usuario = Usuario.objects.get(id=request.user.id)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_productos(request):
    permission_classes = [AllowAny]
    if request.auth:
        queryset = Producto.objects.filter(~Q(id_usuario=request.user.id), vendido=False)
    else:
        queryset = Producto.objects.filter(vendido=False)
    serializer = ProductoSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_producto(request, product_id):
    permission_classes = [IsAuthenticated]
    if request.auth:
        queryset = Producto.objects.filter(id=product_id, id_usuario=request.user.id)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if queryset.exists():
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_producto(request, product_id):
    try:
        producto = Producto.objects.get(id=product_id, id_usuario=request.user.id)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_productos_usuario(request):
    permission_classes = [IsAuthenticated]
    if request.auth:
        queryset = Producto.objects.filter(id_usuario=request.user.id, vendido=False)
    serializer = ProductoSerializer(queryset, many=True)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_productos_usuario_id(request, user_id=None):
    if user_id:
        queryset = Producto.objects.filter(id_usuario=user_id, vendido=False)
    else:
        queryset = Producto.objects.filter(id_usuario=request.user.id, vendido=False)
    serializer = ProductoSerializer(queryset, many=True)
    return Response(serializer.data)

class CategoriasView(APIView):
    def get(self, request):
        categorias = [
            'pantalon', 'camiseta', 'sudadera', 'chaqueta', 
            'cazadora', 'zapato', 'zapatilla', 'accesorio', 'bermuda'
        ]
        return Response(categorias, status=status.HTTP_200_OK)



class BuscarProductoView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'descripcion', 'categoria']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Producto.objects.filter(~Q(id_usuario=self.request.user), vendido=False)
        else:
            return Producto.objects.filter(vendido=False)
class DetailedProductoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Producto.objects.get(id_usuario=self.request.user)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subir_producto(request):
    user = request.user
    data = request.data

    producto = Producto.objects.create(
        nombre=data['nombre'],
        descripcion=data['descripcion'],
        talla=data['talla'],
        categoria=data['categoria'],
        precio=data['precio'],
        imagen=data.get('imagen'),
        imagen2=data.get('imagen2'),
        imagen3=data.get('imagen3'),
        imagen4=data.get('imagen4'),
        imagen5=data.get('imagen5'),
        id_usuario=user
    )

    return Response({"message": "Producto creado con éxito", "producto_id": producto.id})
class CarritoView(generics.ListCreateAPIView):
    serializer_class = CarritoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Carrito.objects.all()
        else:
            return [Carrito.objects.get(id_usuario=self.request.user)]

class DetailedCarritoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Carrito.objects.get(id_usuario=self.request.user)



class GetCarritoView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CarritoSerializer

    def retrieve(self, request, *args, **kwargs):
        carrito = self.get_object()
        serializer = self.get_serializer(carrito)
        data = serializer.data
        data['productos'] = self.get_productos(carrito)
        return Response(data)

    def get_object(self):
        carrito, created = Carrito.objects.get_or_create(id_usuario=self.request.user)
        if not carrito.carritoproducto_set.exists():
            raise NotFound("El carrito está vacío")
        return carrito

    def get_productos(self, carrito):
        productos = carrito.carritoproducto_set.all()
        serializer = CarritoProductoSerializer(productos, many=True)
        return serializer.data

class RemoveCarritoView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, product_id, *args, **kwargs):
        producto = get_object_or_404(Producto, id=product_id)
        usuario = request.user
        carrito = get_object_or_404(Carrito, id_usuario=usuario)
        producto_carrito = get_object_or_404(CarritoProducto, id_carrito=carrito, id_producto=producto)
        producto_carrito.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
def add_cart(request, producto_id):
    producto = Producto.objects.get(pk=producto_id)
    usuario = request.user
    if producto.id_usuario != usuario:
        # Obtener o crear el carrito del usuario
        carrito, creado = Carrito.objects.get_or_create(id_usuario=usuario)

        # Crear o actualizar el producto en el carrito
        carrito_producto, creado = CarritoProducto.objects.get_or_create(id_carrito=carrito, id_producto=producto)
        carrito_producto.save()

        # Calcular el total de productos y el total del precio en el carrito
        total_precio = CarritoProducto.objects.filter(id_carrito=carrito).aggregate(total_precio=Sum('id_producto__precio'))

        response_data = {
            'producto': CarritoProductoSerializer(carrito_producto).data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'No puedes agregar un producto a si mismo'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_carrito_productos(request):
    user = request.user
    carrito = Carrito.objects.filter(id_usuario=user).first()
    if carrito:
        carrito_productos = CarritoProducto.objects.filter(id_carrito=carrito.id)
        serializer = CarritoProductoSerializer(carrito_productos, many=True)
        return Response(serializer.data)
    return Response({'detail': 'Carrito no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class FavoritoView(generics.ListCreateAPIView):
    serializer_class = FavoritoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Favorito.objects.all()
        else:
            return [Favorito.objects.get(id_usuario=self.request.user)]

class DetailedFavoritoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FavoritoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Favorito.objects.get(id_usuario=self.request.user)

@api_view(['POST'])
def add_favorito(request, product_id):
    # Verificar si el usuario y el producto existen
    usuario = request.user
    producto = get_object_or_404(Producto, id=product_id)
    # Verificar si el producto ya está en favoritos del usuario
    favorito_existente = Favorito.objects.filter(id_usuario=usuario, id_producto=producto).exists()
    if favorito_existente:
        return Response({'detail': 'El producto ya está en favoritos'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Crear un nuevo favorito
    favorito = Favorito.objects.create(id_usuario=usuario, id_producto=producto)
    
    # Serializar y devolver la respuesta
    serializer = FavoritoSerializer(favorito)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['GET'])
def get_favoritos(request):
    user = request.user
    favoritos = Favorito.objects.filter(id_usuario=user, id_producto__vendido=False)
    serializer = FavoritoSerializer(favoritos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pedidos(request):
    pedidos = Pedido.objects.filter(id_usuario=request.user)
    pedidos_data = []

    for pedido in pedidos:
        pedido_productos = PedidoProducto.objects.filter(id_pedido=pedido)
        pedido_productos_serializer = PedidoProductoSerializerDialog(pedido_productos, many=True)

        pedido_data = PedidoSerializer(pedido).data
        pedido_data['productos'] = pedido_productos_serializer.data
        pedidos_data.append(pedido_data)

    return Response(pedidos_data)

@api_view(['POST'])
def remove_favorito(request, product_id):
    # Verificar si el usuario y el proyecto existen
    usuario = request.user
    producto = get_object_or_404(Producto, id=product_id)
    # Verificar si el proyecto ya está en favoritos del usuario
    favorito = get_object_or_404(Favorito, id_usuario=usuario, id_producto=producto)
    favorito.delete()

class VentaView(generics.ListCreateAPIView):
    serializer_class = VentaSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Venta.objects.all()
        else:
            return Venta.objects.filter(id_usuario_comprador=self.request.user, id_usuario_vendededor=self.request.user)
        

class DetailedVentaView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Venta.objects.get(id_usuario_comprador=self.request.user, id_usuario_vendededor=self.request.user)

class PagoView(generics.ListCreateAPIView):
    serializer_class = PagoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Pago.objects.all()
        else:
            return [Pago.objects.get(id_usuario=self.request.user)]
    
class DetailedPagoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Pago.objects.get(id_usuario=self.request.user)
class PedidoView(generics.ListCreateAPIView):
    serializer_class = PedidoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Pedido.objects.all()
        else:
            return [Pedido.objects.get(id_usuario=self.request.user)]

class DetailedPedidoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Pedido.objects.get(id_usuario=self.request.user)
    
@api_view(['PATCH'])
def update_pedido_status(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    estado = request.data.get('estado')
    if estado:
        pedido.estado = estado
        pedido.save()
        return Response({'detail': 'Estado de pedido actualizado'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Estado no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

    
class PedidoProductoView(generics.ListCreateAPIView):
    serializer_class = PedidoProductoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return PedidoProducto.objects.all()
        else:
            return [PedidoProducto.objects.get(id_pedido=self.request.user)]

class DetailedPedidoProductoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PedidoProductoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return PedidoProducto.objects.get(id_pedido=self.request.user)
class CarritoProductoView(generics.ListCreateAPIView):
    serializer_class = CarritoProductoSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return CarritoProducto.objects.all()
        else:
            return [CarritoProducto.objects.get(id_carrito=self.request.user)]

class DetailedCarritoProductoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarritoProductoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return CarritoProducto.objects.get(id_carrito=self.request.user)

# Vista para crear pedido

@api_view(['POST'])
def crear_pedido(request):
    user = request.user
    direccion = request.data.get('direccion')
    direccion_facturacion = request.data.get('direccion')
    tipo_pago = request.data.get('tipo_pago')
    nombre_tarjeta = request.data.get('nombre_tarjeta', None)
    num_tarjeta = request.data.get('num_tarjeta', None)
    fecha_vencimiento = request.data.get('fecha_vencimiento', None)
    cvc = request.data.get('cvc', None)

    if not direccion or not direccion_facturacion:
        return Response({"error": "Dirección y dirección de facturación son requeridas"}, status=400)

    # Crear Pago
    pago_data = {
        "id_usuario": user.id,
        "tipo_pago": tipo_pago,
    }

    if tipo_pago == "tarjeta":
        if not nombre_tarjeta or not num_tarjeta or not fecha_vencimiento or not cvc:
            return Response({"error": "Todos los campos de la tarjeta son requeridos para pagos con tarjeta"}, status=400)

        pago_data.update({
            "nombre_tarjeta": nombre_tarjeta,
            "num_tarjeta": num_tarjeta,
            "fecha_vencimiento": fecha_vencimiento,
            "cvc": cvc
        })

    pago_serializer = PagoSerializer(data=pago_data, context={'request': request})
    if pago_serializer.is_valid():
        pago = pago_serializer.save()
    else:
        return Response(pago_serializer.errors, status=400)

    # Crear Pedido
    pedido_data = {
        "id_usuario": user.id,
        "estado": "pagado" if tipo_pago == "tarjeta" else "no pagado",
        "id_pago": pago.id,
        "direccion": direccion,
        "direccion_facturacion": direccion_facturacion,
        "fecha_pedido": time.strftime("%x")
    }

    pedido_serializer = PedidoSerializer(data=pedido_data)
    if pedido_serializer.is_valid():
        pedido = pedido_serializer.save()
    else:
        return Response(pedido_serializer.errors, status=400)
    
    # Obtener productos del carrito
    carrito_productos = CarritoProducto.objects.filter(id_carrito__id_usuario=user)
    carrito_productos_serializer = CarritoProductoSerializer(carrito_productos, many=True)

    # Procesar cada producto en el carrito
    for cp in carrito_productos_serializer.data:
        producto_id = cp['id_producto']['id']
        usuario_vendedor_id = cp['id_producto']['id_usuario']['id']
        
        # Crear PedidoProducto
        pedido_producto_data = {
            "id_pedido": pedido.id,
            "id_producto": producto_id
        }
        pedido_producto_serializer = PedidoProductoSerializer(data=pedido_producto_data)
        if pedido_producto_serializer.is_valid():
            pedido_producto_serializer.save()
        else:
            return Response(pedido_producto_serializer.errors, status=400)

        # Crear Venta
        venta_data = {
            "id_producto": producto_id,
            "id_usuario_comprador": user.id,
            "id_usuario_vendedor": usuario_vendedor_id
        }
        venta_serializer = VentaSerializer(data=venta_data)
        if venta_serializer.is_valid():
            venta_serializer.save()
        else:
            return Response(venta_serializer.errors, status=400)

    # Actualizar productos como vendidos y eliminarlos del carrito
    for cp in carrito_productos:
        producto = cp.id_producto
        cp.delete()
        producto.vendido = True
        producto.save()

    return Response({"message": "Pedido, pago, venta y actualización del producto realizados correctamente"}, status=201)