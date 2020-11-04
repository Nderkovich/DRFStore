from store.models import User, Product, Order
from rest_framework import serializers


# User views serializers
class UserListSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'date_of_birth']

    def save(self, **kwargs):
        user = User.objects.create_user(**self.validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'date_of_birth']

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)
        if password:
            user = User.objects.get(username=self.data['username'])
            user.set_password(password)
            user.save()
        return User.objects.filter(username=self.data['username']).update(**self.validated_data)


# Product views serializers
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# Order views serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
