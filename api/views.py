from django.shortcuts import render
from api.models import *
from api.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UsuarioView(APIView):
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductoView(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

class CarritoView(APIView):
    def get(self, request):
        carritos = Carrito.objects.all()
        serializer = CarritoSerializer(carritos, many=True)
        return Response(serializer.data)

class FavoritoView(APIView):
    def get(self, request):
        favoritos = Favorito.objects.all()
        serializer = FavoritoSerializer(favoritos, many=True)
        return Response(serializer.data)

class VentaView(APIView):
    def get(self, request):
        ventas = Venta.objects.all()
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data)

class PedidoView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.all()
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)
    

# Create your views here.
