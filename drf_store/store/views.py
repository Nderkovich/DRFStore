from store.models import User, Product
from rest_framework import permissions
from store.serializers import ProductSerializer, UserListSerializer, UserDetailSerializer
from store.permissions import UserUpdatePermission
from rest_framework import generics


# User
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]


class UserCreate(generics.CreateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.AllowAny]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [UserUpdatePermission|permissions.IsAdminUser]


# Products
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
