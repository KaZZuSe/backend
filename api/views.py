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
    """

    Devuelve una lista de todos los usuarios en caso de
    que el usuario sea administrador, o solo el usuario
    autenticado en caso de que sea ese usuario.

    """
    serializer_class = UsuarioSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            # Si el usuario es administrador, devolver todos los usuarios
            return Usuario.objects.all()
        else:
            # Si el usuario no es administrador, devolver solo el usuario autenticado (ha realizado la request)
            return [self.request.user]
        
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_info(request, user_id):
    """

    Devuelve la información de un usuario en particular.
    En caso de que el usuario no exista, devolvera un error 404.

    """
    try:
        usuario = Usuario.objects.get(id=user_id)
        # Si el usuario existe, devolver sus datos
        data = {
            'id': usuario.id,
            'username': usuario.username,
            'fecha_creacion': usuario.fecha_creacion,
            'imagen': usuario.imagen.url if usuario.imagen else None,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Usuario.DoesNotExist:
        # Si el usuario no existe, devolver un error 404
        return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
class DetailedUsuarioView(generics.RetrieveUpdateDestroyAPIView):
    """

    Devuelve la información de un usuario en particular.

    """
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """

        Devuelve el objeto de usuario correspondiente al usuario autenticado

        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """

        Encripta la contraseña del usuario autenticado

        """
        
        user = self.get_object()
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            request.data.pop('password')
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """

        Actualiza la contraseña del usuario autenticado

        """
        user = self.get_object()
        if 'password' in request.data:
            # Encriptar la contraseña
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
        """
        
        Crea un nuevo usuario y lo autentica.
        
        """ 
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Crea el usuario
            user = Usuario.objects.get(username=request.data['username'])
            # Encriptar la contraseña
            user.set_password(request.data['password'])
            # Guardar el usuario
            user.save()
            # Crear el token
            token = Token.objects.create(user=user)
            # Serializar y devolver la respuesta
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
    """	

    Autentica un usuario y devuelve su token de acceso.

    """
    user = get_object_or_404(Usuario, username=request.data.get('username'))
    # Comprobar la contraseña del usuario
    if not user.check_password(request.data.get('password')):
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    # Crear el token de acceso o reutilizar uno existente
    token, created = Token.objects.get_or_create(user=user)
    serializer = UsuarioSerializer(instance=user)
    return Response({'token': token.key,'user': serializer.data}, status=status.HTTP_200_OK)
@api_view(['GET'])
def logout(request):
    """

    Elimina el token de acceso del usuario autenticado.

    """
    token = request.auth
    if token:
        token.delete()
    return Response(status=status.HTTP_200_OK)
class ProductoView(generics.ListCreateAPIView):
    """

    Crea un nuevo producto.

    """	
    serializer_class = ProductoSerializer
    def get_queryset(self):
        """

        Devuelve todos los productos excepto los vendidos.

        """	
        if self.request.user.is_authenticated:
            # Si el usuario esta autenticado, devolver todos los productos excepto los vendidos y del usuario autenticado
            queryset = Producto.objects.filter(~Q(id_usuario=self.request.user.id), vendido=False)
        else:
            # Si el usuario no esta autenticado, devolver todos los productos excepto los vendidos
            queryset = Producto.objects.filter(vendido=False)
        return queryset

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_usuario(request):
    """
    
    Elimina el usuario autenticado.
    
    """
    try:
        # Obtener el usuario autenticado
        usuario = Usuario.objects.get(id=request.user.id)
        # Eliminar el usuario
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Usuario.DoesNotExist:
        # Devolver un error 404 si el usuario no existe
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_usuario(request):
    """

    Actualiza el usuario autenticado.

    """
    try:
        # Obtener el usuario autenticado
        usuario = Usuario.objects.get(id=request.user.id)
    except Usuario.DoesNotExist:
        # Devolver un error 404 si el usuario no existe
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Actualizar los datos del usuario
    serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
    # Validar los datos del usuario
    if serializer.is_valid():
        # Guardar los cambios
        serializer.save()
        return Response(serializer.data)
    # Devolver un error 400 si los datos del usuario no son válidos
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_productos(request):
    """

    Devuelve todos los productos excepto los vendidos.

    """
    permission_classes = [AllowAny]
    if request.auth:
        # Si el usuario esta autenticado, devolver todos los productos excepto los vendidos y del usuario autenticado
        queryset = Producto.objects.filter(~Q(id_usuario=request.user.id), vendido=False)
    else:
        # Si el usuario no esta autenticado, devolver todos los productos excepto los vendidos	
        queryset = Producto.objects.filter(vendido=False)
    serializer = ProductoSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_producto(request, product_id):
    """

    Elimina un producto pertenieciente al usuario autenticado.

    """
    permission_classes = [IsAuthenticated]
    # Obtener el usuario autenticado
    if request.auth:
        # Devuelve todos los productos del usuario
        queryset = Producto.objects.filter(id=product_id, id_usuario=request.user.id)
    else:
        # Sino devuelve un error 401
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if queryset.exists():
        # Eliminar el producto si existe
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_producto(request, product_id):
    """

    Actualiza un producto pertenieciente al usuario autenticado.

    """
    try:
        # Obtener el producto del usuario autenticado
        producto = Producto.objects.get(id=product_id, id_usuario=request.user.id)
    except Producto.DoesNotExist:
        # Devolver un error 404 si el producto no existe
        return Response(status=status.HTTP_404_NOT_FOUND)
    # Actualizar los datos del producto
    serializer = ProductoSerializer(producto, data=request.data, partial=True)
    if serializer.is_valid():
        # Guardar los cambios
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_productos_usuario(request):
    """

    Devuelve todos los productos del usuario autenticado.

    """
    permission_classes = [IsAuthenticated]
    if request.auth:
        # Filtra los productos del usuario autenticado
        queryset = Producto.objects.filter(id_usuario=request.user.id, vendido=False)
    # Sino devuelve un error 401
    serializer = ProductoSerializer(queryset, many=True)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_productos_usuario_id(request, user_id=None):
    """

    Devuelve todos los productos del usuario buscado.

    """
    if user_id:
        # Filtra los productos del usuario buscado
        queryset = Producto.objects.filter(id_usuario=user_id, vendido=False)
    else:
        # Filtra los productos del usuario autenticado
        queryset = Producto.objects.filter(id_usuario=request.user.id, vendido=False)
    # Sino devuelve un error 401
    serializer = ProductoSerializer(queryset, many=True)
    return Response(serializer.data)

class CategoriasView(APIView):
    def get(self, request):
        """

        Devuelve todas las categorias.

        """
        categorias = [
            'pantalon', 'camiseta', 'sudadera', 'chaqueta', 
            'cazadora', 'zapato', 'zapatilla', 'accesorio', 'bermuda'
        ]
        return Response(categorias, status=status.HTTP_200_OK)



class BuscarProductoView(generics.ListAPIView):
    # Permisos para buscar productos todos los usuarios
    permission_classes = [AllowAny]
    # Serializador para la lista de productos
    serializer_class = ProductoSerializer
    # Filtro los productos por nombre, descripción y categoría
    filter_backends = [SearchFilter]
    search_fields = ['nombre', 'descripcion', 'categoria']

    def get_queryset(self):
        """

        Devuelve todos los productos excepto los vendidos que coinciden con la busqueda.

        """	
        if self.request.user.is_authenticated:
            # Si el usuario esta autenticado, devolver todos los productos excepto los vendidos y del usuario autenticado relacionados a la búsqueda
            return Producto.objects.filter(~Q(id_usuario=self.request.user), vendido=False)
        else:
            return Producto.objects.filter(vendido=False)
class DetailedProductoView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """

        Devuelve el producto del usuario autenticado.

        """		
        return Producto.objects.get(id_usuario=self.request.user)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subir_producto(request):
    """

    Crea un nuevo producto para el usuario autenticado.

    """	
    # Obtener el usuario autenticado
    user = request.user
    # Crear el nuevo producto
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
        """

        Devuelve todos los carritos del usuario autenticado.

        """
        if self.request.user.is_superuser:
            # Si el usuario es administrador, devolver todos los carritos
            return Carrito.objects.all()
        else:
            # Si el usuario no es administrador, devolver solo los carritos del usuario autenticado
            return [Carrito.objects.get(id_usuario=self.request.user)]

class DetailedCarritoView(generics.RetrieveUpdateDestroyAPIView):
    # Permisos para buscar productos todos los usuarios
    serializer_class = CarritoSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """

        Devuelve el carrito del usuario autenticado.

        """
        # Devuelve el carrito del usuario autenticado 
        return Carrito.objects.get(id_usuario=self.request.user)



class GetCarritoView(generics.RetrieveAPIView):
    # Permisos para obtener el carrito de un usuario autenticado
    permission_classes = [IsAuthenticated]
    serializer_class = CarritoSerializer

    def retrieve(self, request, *args, **kwargs):
        """

        Devuelve el carrito del usuario autenticado.

        """
        # Devuelve el carrito	
        carrito = self.get_object()
        # Serializa el carrito
        serializer = self.get_serializer(carrito)
        # Obtiene los productos del carrito
        data = serializer.data
        # Devuelve los productos del carrito
        data['productos'] = self.get_productos(carrito)
        return Response(data)

    def get_object(self):
        """

        Devuelve el carrito del usuario autenticado.

        """
        # Crea un nuevo carrito si no existe
        carrito, created = Carrito.objects.get_or_create(id_usuario=self.request.user)
        if not carrito.carritoproducto_set.exists():
            # Si el carrito no tiene productos, levantar una excepción
            raise NotFound("El carrito está vacío")
        return carrito

    def get_productos(self, carrito):
        """

        Devuelve los productos del carrito.

        """
        productos = carrito.carritoproducto_set.all()
        # Serializa los productos del carrito
        serializer = CarritoProductoSerializer(productos, many=True)
        return serializer.data

class RemoveCarritoView(generics.DestroyAPIView):
    # Permisos para borrar un producto solo al usuario autenticado
    permission_classes = [IsAuthenticated]
    def delete(self, request, product_id, *args, **kwargs):
        """

        Borra el producto del carrito del usuario autenticado.

        """
        # Obtener el producto del usuario
        producto = get_object_or_404(Producto, id=product_id)
        # Obtener el usuario autenticado
        usuario = request.user
        # Obtener el carrito del usuario
        carrito = get_object_or_404(Carrito, id_usuario=usuario)
        # Obtener el producto del carrito
        producto_carrito = get_object_or_404(CarritoProducto, id_carrito=carrito, id_producto=producto)
        # Borrar el producto del carrito
        producto_carrito.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
def add_cart(request, producto_id):
    """

    Agrega un producto al carrito del usuario autenticado.

    """
    # Obtener el producto	    
    producto = Producto.objects.get(pk=producto_id)
    # Obtener el usuario autenticado
    usuario = request.user
    # Comprobar si el usuario es el propietario del producto
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
    # Verificar si el usuario y el producto existen
    usuario = request.user
    producto = get_object_or_404(Producto, id=product_id)
    # Verificar si el producto ya está en favoritos del usuario
    favorito = get_object_or_404(Favorito, id_usuario=usuario, id_producto=producto)
    favorito.delete()

class VentaView(generics.ListCreateAPIView):
    # Serializar Ventas
    serializer_class = VentaSerializer
    def get_queryset(self):
        """	

        Obtener las ventas del usuario actual
        
        """
        if self.request.user.is_superuser:
            return Venta.objects.all()
        else:
            return Venta.objects.filter(id_usuario_comprador=self.request.user, id_usuario_vendededor=self.request.user)
        

class DetailedVentaView(generics.RetrieveUpdateDestroyAPIView):
    # Serializar Ventas
    serializer_class = VentaSerializer
    # Permisos 
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """

        Obtener las ventas del usuario actual

        """
        return Venta.objects.get(id_usuario_comprador=self.request.user, id_usuario_vendededor=self.request.user)

class PagoView(generics.ListCreateAPIView):
    # Serializar Pagos
    serializer_class = PagoSerializer
    def get_queryset(self):
        """

        Obtener los pagos del usuario actual

        """	
        if self.request.user.is_superuser:
            # Si el usuario es administrador, devolver todos los pagos
            return Pago.objects.all()
        else:
            # Si el usuario no es administrador, devolver solo sus pagos
            return [Pago.objects.get(id_usuario=self.request.user)]
    
class DetailedPagoView(generics.RetrieveUpdateDestroyAPIView):
    # Serializar Pagos
    serializer_class = PagoSerializer
    # Permisos
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """

        Obtener los pagos del usuario actual

        """
        return Pago.objects.get(id_usuario=self.request.user)
class PedidoView(generics.ListCreateAPIView):
    # Serializar Pedidos
    serializer_class = PedidoSerializer
    def get_queryset(self):
        """

        Obtener los pedidos del usuario actual

        """
        if self.request.user.is_superuser:
            # Si el usuario es administrador, devolver todos los pedidos
            return Pedido.objects.all()
        else:
            # Si el usuario no es administrador, devolver solo sus pedidos
            return [Pedido.objects.get(id_usuario=self.request.user)]

class DetailedPedidoView(generics.RetrieveUpdateDestroyAPIView):
    # Serializar Pedidos
    serializer_class = PedidoSerializer
    # Permisos
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """

        Obtener los pedidos del usuario actual

        """
        return Pedido.objects.get(id_usuario=self.request.user)
    
@api_view(['PATCH'])
def update_pedido_status(request, pedido_id):
    """

    Actualizar el estado de un pedido

    """
    # Obtener el pedido por su ID, sino devolver error
    pedido = get_object_or_404(Pedido, id=pedido_id)
    # Actualizar el estado del pedido
    estado = request.data.get('estado')
    if estado:
        # Verificar que el estado sea válido
        pedido.estado = estado
        # Guardar los cambios
        pedido.save()
        return Response({'detail': 'Estado de pedido actualizado'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Estado no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

    
class PedidoProductoView(generics.ListCreateAPIView):
    # Serializar PedidoProducto
    serializer_class = PedidoProductoSerializer
    def get_queryset(self):
        """

        Obtener los pedidos del usuario actual

        """
        if self.request.user.is_superuser:
            # Si el usuario es administrador, devolver todos los pedidosproductos
            return PedidoProducto.objects.all()
        else:
            # Si el usuario no es administrador, devolver solo sus pedidosproductos
            return [PedidoProducto.objects.get(id_pedido=self.request.user)]

class DetailedPedidoProductoView(generics.RetrieveUpdateDestroyAPIView):
    # Serializar PedidoProducto
    serializer_class = PedidoProductoSerializer
    # Permisos
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """

        Obtener los pedidos del usuario actual

        """
        return PedidoProducto.objects.get(id_pedido=self.request.user)
class CarritoProductoView(generics.ListCreateAPIView):
    # Serializar CarritoProducto
    serializer_class = CarritoProductoSerializer
    def get_queryset(self):
        """

        Obtener los carritosproductos del usuario actual

        """
        if self.request.user.is_superuser:
            # Si el usuario es administrador, devolver todos los carritosproductos
            return CarritoProducto.objects.all()
        else:
            # Si el usuario no es administrador, devolver solo sus carritosproductos
            return [CarritoProducto.objects.get(id_carrito=self.request.user)]

class DetailedCarritoProductoView(generics.RetrieveUpdateDestroyAPIView):
    # Serializar CarritoProducto
    serializer_class = CarritoProductoSerializer
    # Permisos
    permission_classes = [IsAuthenticated]
    def get_object(self):
        """

        Obtener los carritos del usuario actual

        """
        return CarritoProducto.objects.get(id_carrito=self.request.user)

# Vista para crear pedido

@api_view(['POST'])
def crear_pedido(request):
    """

    Crear un nuevo pedido cogiendo los datos del usuario
    inscribiendo en las tablas correspondientes
    en pago: el metodo de pago
    en pedido: los datos del pedido (direccion, total, etc)
    en pedidoproducto: los productos del pedido
    en venta: los datos de la venta (usuario vendedor, usuario comprador, etc)

    """

    # Obtener datos	
    user = request.user
    # Validar datos del formulario
    direccion = request.data.get('direccion')
    direccion_facturacion = request.data.get('direccion')
    tipo_pago = request.data.get('tipo_pago')
    nombre_tarjeta = request.data.get('nombre_tarjeta', None)
    num_tarjeta = request.data.get('num_tarjeta', None)
    fecha_vencimiento = request.data.get('fecha_vencimiento', None)
    cvc = request.data.get('cvc', None)

    # Validar que se haya escrito la dirección y la dirección de facturación
    if not direccion or not direccion_facturacion:
        return Response({"error": "Dirección y dirección de facturación son requeridas"}, status=400)

    # Crear Pago
    pago_data = {
        "id_usuario": user.id, # guarda el id del usuario
        "tipo_pago": tipo_pago, # guarda el tipo de pago
    }

    # Compueba si el tipo de pago es tarjeta
    if tipo_pago == "tarjeta":
        # Si el pago es tarjeta, se debe proporcionar los datos de la tarjeta
        if not nombre_tarjeta or not num_tarjeta or not fecha_vencimiento or not cvc:
            return Response({"error": "Todos los campos de la tarjeta son requeridos para pagos con tarjeta"}, status=400)
        # Se actualiza el objeto de pago con los datos de la tarjeta
        pago_data.update({
            "nombre_tarjeta": nombre_tarjeta, # Guarda el nombre de la tarjeta
            "num_tarjeta": num_tarjeta, # Guarda el número de la tarjeta
            "fecha_vencimiento": fecha_vencimiento, # Guarda la fecha de vencimiento
            "cvc": cvc # Guarda el CVC
        })
    # Se valida el objeto de pago
    pago_serializer = PagoSerializer(data=pago_data, context={'request': request})
    if pago_serializer.is_valid():
        # Se guarda el objeto de pago
        pago = pago_serializer.save()
    else:
        return Response(pago_serializer.errors, status=400)

    # Crear Pedido
    pedido_data = {
        "id_usuario": user.id, # Guarda el id del usuario
        "estado": "pagado" if tipo_pago == "tarjeta" else "no pagado", # Guarda el estado del pedido
        "id_pago": pago.id, # Guarda el id del pago
        "direccion": direccion, # Guarda la dirección
        "direccion_facturacion": direccion_facturacion, # Guarda la dirección de facturación
        "fecha_pedido": time.strftime("%x") # Guarda la fecha
    }
    # Serializar el objeto de pedido
    pedido_serializer = PedidoSerializer(data=pedido_data)
    # Validar el objeto de pedido
    if pedido_serializer.is_valid():
        # Guardar el objeto de pedido
        pedido = pedido_serializer.save()
    else:
        # Devolver los errores del objeto de pedido
        return Response(pedido_serializer.errors, status=400)
    
    # Obtener productos del carrito
    carrito_productos = CarritoProducto.objects.filter(id_carrito__id_usuario=user)
    carrito_productos_serializer = CarritoProductoSerializer(carrito_productos, many=True)

    # Procesar cada producto en el carrito
    for cp in carrito_productos_serializer.data:
        producto_id = cp['id_producto']['id'] # Obtener el id del producto
        usuario_vendedor_id = cp['id_producto']['id_usuario']['id'] # Obtener el id del usuario vendedor
        
        # Crear PedidoProducto
        pedido_producto_data = {
            "id_pedido": pedido.id, # Guarda el id del pedido
            "id_producto": producto_id # Guarda el id del producto
        }

        # Serializar el objeto de pedidoproducto
        pedido_producto_serializer = PedidoProductoSerializer(data=pedido_producto_data)

        # Validar el objeto de pedidoproducto
        if pedido_producto_serializer.is_valid():
            # Guardar el objeto de pedidoproducto
            pedido_producto_serializer.save()
        else:
            return Response(pedido_producto_serializer.errors, status=400)

        # Crear Venta
        venta_data = {
            "id_producto": producto_id, # Guarda el id del producto
            "id_usuario_comprador": user.id, # Guarda el id del usuario
            "id_usuario_vendedor": usuario_vendedor_id # Guarda el id del usuario
        }

        # Serializar el objeto de venta
        venta_serializer = VentaSerializer(data=venta_data)

        # Validar el objeto de venta
        if venta_serializer.is_valid():
            # Guardar el objeto de venta
            venta_serializer.save()
        else:
            # Devolver los errores del objeto de venta
            return Response(venta_serializer.errors, status=400)

    # Actualizar productos como vendidos y eliminarlos del carrito
    for cp in carrito_productos:
        # Obtener el objeto de producto
        producto = cp.id_producto
        # Eliminar el objeto de carrito
        cp.delete()
        # Marcar el producto como vendido para que no se pueda agregar de nuevo
        producto.vendido = True
        # Guardar los cambios
        producto.save()

    return Response({"message": "Pedido, pago, venta y actualización del producto realizados correctamente"}, status=201)