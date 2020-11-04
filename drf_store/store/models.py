from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Role(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=10)


class User(AbstractBaseUser):
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=False)

    roles = models.ManyToManyField(Role)

    USERNAME_FIELD = 'username'


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
