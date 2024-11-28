from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя."""

    def create_user(self, email, password=None, name = None, **extra_fields):
        """Создает и возвращает обычного пользователя."""
        extra_fields.setdefault('is_staff', False)
        if not email:
            raise ValueError('Email обязателен для пользователя.')
        if not name:
            raise ValueError('Имя (name) обязательно для пользователя.')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name = name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None, **extra_fields):
        """Создает и возвращает суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(email, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    email = models.EmailField(unique=True, verbose_name='E-mail')
    name = models.CharField(max_length=255, verbose_name='Имя')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Ученик')  # Для доступа к админке
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Поля, обязательные кроме email и password

    objects = CustomUserManager()

    def __str__(self):
        return self.email
