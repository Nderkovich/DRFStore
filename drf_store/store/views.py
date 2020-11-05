from store.models import User, Order
from rest_framework import permissions
from store.serializers import UserDetailSerializer, OrderSerializer, UserCreateSerializer
from store.permissions import UserUpdatePermission, OrderOwnerPermission, OrderChangePermission
from rest_framework import generics


# User
class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [UserUpdatePermission]


# Orders
class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
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
