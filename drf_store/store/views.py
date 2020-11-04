from store.models import User, Product, Order
from rest_framework import permissions
from store.serializers import ProductSerializer, UserListSerializer, UserDetailSerializer, OrderSerializer, OrderAdminSerializer
from store.permissions import UserUpdatePermission, OrderOwnerPermission, OrderChangePermission
from rest_framework import generics


# User
class UserList(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all()
        noorders = self.request.query_params.get('noorders', None)
        if noorders == 'true':
            queryset = queryset.filter(order=None)
        return queryset


class UserCreate(generics.CreateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.AllowAny]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [UserUpdatePermission | permissions.IsAdminUser]


# Products
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


# Orders
class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs)
        return Order.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'PUT':
            self.permission_classes = [OrderChangePermission]
        self.permission_classes.append(OrderOwnerPermission)

        return super(OrderDetail, self).get_permissions()


class OrderAdminList(generics.ListCreateAPIView):
    serializer_class = OrderAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Order.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class OrderAdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderAdminSerializer
    permission_classes = [permissions.IsAdminUser]
