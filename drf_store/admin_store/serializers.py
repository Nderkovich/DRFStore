from store.models import User, Role, Product, Order
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Role
        fields = ['name']


class AdminUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_of_birth', 'create_time', 'update_time', 'roles']


class AdminUserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'date_of_birth', 'create_time', 'update_time', 'roles']

    def save(self, **kwargs):
        password = self.validated_data.pop('password', None)
        if password:
            user = User.objects.get(username=self.data['username'])
            user.set_password(password)
            user.save()
        return User.objects.filter(username=self.data['username']).update(**self.validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderAdminSerializer(serializers.ModelSerializer):
    ADMIN_ALLOWED_STATUS = ('IN_PROGRESS', 'APPROVED', 'DECLINED')
    status = serializers.ChoiceField(choices=ADMIN_ALLOWED_STATUS)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'status', 'products', 'user', 'create_time', 'update_time']
