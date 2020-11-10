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
    def _create_user(self, username, password, date_of_birth, roles: List[Role], **extra_fields):
        values = [date_of_birth]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        username = self.normalize_email(username)
        user = self.model(
            username=username,
            **field_value_map,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        for role in roles:
            user.roles.add(role.id)
        return user

    def create_user(self, username, password, date_of_birth, **extra_fields):
        roles = [Role.objects.get(name=Role.CLIENT)]
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, date_of_birth, roles, **extra_fields)

    def create_superuser(self, username,  password, date_of_birth, **extra_fields):
        roles = [Role.objects.get(name=Role.ADMIN), Role.objects.get(name=Role.CLIENT)]
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, date_of_birth, roles,  **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=False)

    roles = models.ManyToManyField(Role)

    @property
    def is_staff(self):
        return self.roles.filter(name=Role.ADMIN).exists()

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        return super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['date_of_birth']

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
