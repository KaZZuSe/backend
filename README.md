# Proyecto Backend con Django

Este proyecto está desarrollado con Django, usando diversas librerías como DjangoRestFramework para la salida de endpoints.
## Próposito del proyecto

Aplicación backend de ecommerce que conecta con el servicio frontend programado en Reacr


## 🚀 Configuración y ejecución

### 1️⃣ Clonar el repositorio y acceder a el
```sh
git clone https://github.com/useemtn/backend.git
```
```sh
cd .\backend
```
### 2️⃣ Crear un entorno virtual en Python
```sh
python -m venv venv
```
### 3️⃣ Activar el entorno virtual
```sh
.\venv\Scripts\activate
```
### 4️⃣ Instalar las dependencias del proyecto
```sh
pip install -r .\requirements.txt
```
### 5️⃣ Generar las migraciones de la base de datos
```sh
python .\manage.py makemigrations
```
### 6️⃣ Aplicar las migraciones
```sh
python .\manage.py migrate
```
### 7️⃣ Ejecutar el servidor de desarrollo
```sh
python .\manage.py runserver
```
## 📌 Notas
Asegúrate de tener Docker y Python correctamente instalados en tu sistema.
