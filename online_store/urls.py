"""
URL configuration for online_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views import (
    product_list, product_detail,
    category_list, category_detail,
    customer_list, customer_detail,
    inventory_list, inventory_detail,
    cartitem_list, cartitem_detail,
    order_list, order_detail,
    orderdetail_list, orderdetail_detail,
    stockbalance_list, stockbalance_detail,
    register,
)
from django.shortcuts import render


def home_view(request):
    return render(request, 'home.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('categories/', category_list, name='category_list'),
    path('categories/<int:pk>/', category_detail, name='category_detail'),
    path('customers/', customer_list, name='customer_list'),
    path('customers/<int:pk>/', customer_detail, name='customer_detail'),
    path('inventory/', inventory_list, name='inventory_list'),
    path('inventory/<int:pk>/', inventory_detail, name='inventory_detail'),
    path('cartitems/', cartitem_list, name='cartitem_list'),
    path('cartitems/<int:pk>/', cartitem_detail, name='cartitem_detail'),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:pk>/', order_detail, name='order_detail'),
    path('orderdetails/', orderdetail_list, name='orderdetail_list'),
    path('orderdetails/<int:pk>/', orderdetail_detail, name='orderdetail_detail'),
    path('stockbalances/', stockbalance_list, name='stockbalance_list'),
    path('stockbalances/<int:pk>/', stockbalance_detail, name='stockbalance_detail'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
