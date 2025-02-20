from django.urls import path
from . import views

app_name = 'catalog'  # Пространство имён для URL

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('tool/<int:pk>/', views.tool_detail, name='tool_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('register/', views.register, name='register'),
    path('add-tool/', views.add_tool, name='add_tool'),  # Убедитесь, что этот маршрут есть
]