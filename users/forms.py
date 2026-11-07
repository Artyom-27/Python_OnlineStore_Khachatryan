from django import forms
from .models import Product, Category, Customer, Inventory, Order, OrderDetail, StockBalance

class CartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'email',
                  'country', 'city', 'street', 'house_number', 'apartment_number', 'postal_code']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'quantity_in_stock', 'warehouse_section']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'order_status', 'total_amount']


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'quantity', 'price_at_purchase']


class StockBalanceForm(forms.ModelForm):
    class Meta:
        model = StockBalance
        fields = ['product', 'quantity', 'reserved_quantity', 'minimum_stock', 'last_restocked']

