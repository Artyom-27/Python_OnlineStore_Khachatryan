from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Customer, Product, Category, Inventory, CartItem, Order, OrderDetail

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderDetail)
