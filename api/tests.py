from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Producto, Carrito, CarritoProducto, Pedido, Favorito

# Caso de prueba para la creación de usuarios
class UserCreationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_creation(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'direccion': '123 Test St'
        }
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email, 'testuser@example.com')

# Caso de prueba para el login de usuarios
class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )

    def test_user_login(self):
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

# Caso de prueba para la creación de productos
class ProductCreationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_product_creation(self):
        data = {
            'nombre': 'Test Product',
            'descripcion': 'Test Description',
            'talla': 'M',
            'categoria': 'camiseta',
            'precio': '10.00'
        }
        response = self.client.post('/api/productos/add/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Issue here
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Producto.objects.get().nombre, 'Test Product')


# Caso de prueba para obtener productos disponibles
class GetAvailableProductsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )
        Producto.objects.create(
            nombre='Test Product', 
            descripcion='Test Description', 
            talla='M', 
            categoria='camiseta', 
            precio='10.00', 
            id_usuario=self.user
        )

    def test_get_available_products(self):
        response = self.client.get('/api/productos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

# Caso de prueba para agregar productos al carrito
class AddProductToCartTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )
        self.user2 = get_user_model().objects.create_user(
            username='testuser2',
            first_name='Test',
            last_name='User',
            email='testuser2@example.com',
            direccion='123 Test St',
            password='password123'
        )
        self.client.force_authenticate(user=self.user2)
        self.product = Producto.objects.create(
            nombre='Test Product', 
            descripcion='Test Description', 
            talla='M', 
            categoria='camiseta', 
            precio='10.00', 
            id_usuario=self.user
        )

    def test_add_product_to_cart(self):
        url = f'/api/carrito/add/{self.product.id}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(CarritoProducto.objects.filter(id_producto=self.product, id_carrito__id_usuario=self.user2).exists())

# Caso de prueba para la creación de pedidos
class CreateOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)
        self.product = Producto.objects.create(
            nombre='Test Product', 
            descripcion='Test Description', 
            talla='M', 
            categoria='camiseta', 
            precio='10.00', 
            id_usuario=self.user
        )
        self.cart = Carrito.objects.create(id_usuario=self.user)
        CarritoProducto.objects.create(id_carrito=self.cart, id_producto=self.product)

    def test_create_order(self):
        data = {
            'direccion': '123 Test St',
            'tipo_pago': 'contrarreembolso'
        }
        response = self.client.post('/api/crear_pedido/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Pedido.objects.filter(id_usuario=self.user).exists())

# Caso de prueba para agregar productos a favoritos
class AddProductToFavoritesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)
        self.product = Producto.objects.create(
            nombre='Test Product', 
            descripcion='Test Description', 
            talla='M', 
            categoria='camiseta', 
            precio='10.00', 
            id_usuario=self.user
        )

    def test_add_product_to_favorites(self):
        url = f'/api/favoritos/add/{self.product.id}/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorito.objects.filter(id_producto=self.product).exists())

# Caso de prueba para la actualización de usuarios
class UserUpdateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_user_update(self):
        data = {
            'first_name': 'Updated'
        }
        response = self.client.patch('/api/usuarios/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

# Caso de prueba para la eliminación de usuarios
class RemoveUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            direccion='123 Test St',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_remove_user(self):
        response = self.client.delete('/api/usuarios/remove/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(get_user_model().objects.filter(username='testuser').exists())
