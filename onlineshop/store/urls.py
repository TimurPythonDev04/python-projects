from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import product_list, product_detail, category_products, cart_detail, add_to_cart, clear_cart

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('category/<int:pk>/', category_products, name='category_products'),
    path('cart/', cart_detail, name='cart_detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/clear/', clear_cart, name='clear_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
]




