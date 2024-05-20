from django.contrib.auth.models import BaseUserManager

class UserCustomManager(BaseUserManager):
    """
    Administrador de usuarios personalizado para este proyecto.
    """
    def create_user(self,username, first_name, last_name, email, password,direccion, **extra_fields):
        """
        Crear y guardar un usuario con el email y password proporcionado.
        """
        if not email:
            raise ValueError('Debes introducir un email')
        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            direccion=direccion,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,first_name, last_name, email, password,**extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Super usuario debe tener is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Super usuario debe tener is_superuser=True.'))

        return self.create_user(username,first_name, last_name, email, password, **extra_fields)