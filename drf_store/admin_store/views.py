from store.models import User, Product, Order
from rest_framework import generics, permissions, viewsets
from admin_store.serializers import AdminUserListSerializer, AdminUserDetailSerializer, ProductSerializer, \
    OrderAdminSerializer


# User
class UserList(generics.ListAPIView):
    serializer_class = AdminUserListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.all()
        noorders = self.request.query_params.get('noorders', None)
        if noorders == 'true':
            queryset = queryset.filter(order=None)
        return queryset


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserDetailSerializer
    permission_classes = [permissions.IsAdminUser]


# Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


# Order
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Order.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
