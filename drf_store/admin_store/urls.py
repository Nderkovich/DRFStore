from django.urls import path, include
from admin_store import views
from rest_framework.routers import DefaultRouter

app_name = 'admin_store'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')
router.register(r'orders', views.OrderViewSet, basename='orders')

urlpatterns = [
    path('users/', views.UserList.as_view(), name='admin_user_list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='admin_user_detail'),
    path('', include(router.urls))
]
