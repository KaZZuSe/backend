from django.contrib.auth.models import BaseUserManager

class UserCustomManager(BaseUserManager):
    """
    Administrador de usuarios personalizado para este proyecto.

    """
    def create_user(self,username, first_name, last_name, email, password,direccion, **extra_fields):
        """
        Crear y guardar un usuario con el email y contraseña proporcionado.

        """
        if not email:
            raise ValueError('Debes introducir un email')
        email = self.normalize_email(email)
        # Crear el usuario seguido de los campos extras
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            direccion=direccion,
            **extra_fields
        )
        # Encriptar la contraseña y guardar el usuario
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,first_name, last_name, email, password,**extra_fields):
        """
        Crear y guardar un super usuario con el email y contraseña proporcionado.

        """
        # Definir los campos extras	
        extra_fields.setdefault('is_staff', True)
        # Establecer is_superuser como True
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Super usuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Super usuario debe tener is_superuser=True.'))

        return self.create_user(username,first_name, last_name, email, password, **extra_fields)