from typing import List

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Role(models.Model):
    CLIENT = 'Client'
    ADMIN = 'Admin'

    ROLES = (
        (CLIENT, 'Client'),
        (ADMIN, 'Admin')
    )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=10, choices=ROLES)


class UserManager(BaseUserManager):
    def _create_user(self, password, email, roles: List[Role], **extra_fields):
        if not password or len(password) < 8:
            raise ValueError('Password length is invalid')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.clean_fields()
        user.save(using=self._db)
        for role in roles:
            user.roles.add(role.id)
        return user

    def create_user(self, password, email, **extra_fields):
        roles = [Role.objects.get(name=Role.CLIENT)]
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, email, roles, **extra_fields)

    def create_superuser(self, password, email, **extra_fields):
        roles = [Role.objects.get(name=Role.ADMIN)]
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(password, email, roles, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=70, blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(blank=False, null=False)

    roles = models.ManyToManyField(Role)

    @property
    def is_staff(self):
        return self.roles.filter(name=Role.ADMIN).exists()

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        return super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['date_of_birth', 'email']

    objects = UserManager()


class Product(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)


class Order(models.Model):
    STATUSES = (
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('FINISHED', 'FINISHED'),
        ('APPROVED', 'APPROVED'),
        ('DECLINED', 'DECLINED')
    )
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=15, choices=STATUSES, default='IN_PROGRESS')

    products = models.ManyToManyField(Product)
