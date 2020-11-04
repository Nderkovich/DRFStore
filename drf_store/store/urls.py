from django.urls import path
from store import views


app_name = 'api'


urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='user_add'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('orders/', views.OrderList.as_view(), name='order_list'),
    path('orders/<int:pk>', views.OrderDetail.as_view(), name='order_detail'),
    path('admin/orders/', views.OrderAdminList.as_view(), name='order_admin_list'),
    path('admin/orders/<int:pk>', views.OrderAdminDetail.as_view(), name='order_admin_detail'),
]
