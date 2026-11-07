from django.shortcuts import render, redirect
from .models import Product, Category, Customer, Inventory, CartItem, Order, OrderDetail, StockBalance
from .forms import CartForm
from .models import Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    context = {'product': product}
    return render(request, 'product_detail.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category_list.html', context)


def category_detail(request, pk):
    category = Category.objects.get(pk=pk)
    context = {'category': category}
    return render(request, 'category_detail.html', context)


def customer_list(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'customer_list.html', context)


def customer_detail(request, pk):
    customer = Customer.objects.get(pk=pk)
    context = {'customer': customer}
    return render(request, 'customer_detail.html', context)


def inventory_list(request):
    inventories = Inventory.objects.all()
    context = {'inventories': inventories}
    return render(request, 'inventory_list.html', context)


def inventory_detail(request, pk):
    inventory = Inventory.objects.get(pk=pk)
    context = {'inventory': inventory}
    return render(request, 'inventory_detail.html', context)


def cartitem_list(request):
    cartitems = CartItem.objects.all()
    context = {'cartitems': cartitems}
    return render(request, 'cartitem_list.html', context)


def cartitem_detail(request, pk):
    cartitem = CartItem.objects.get(pk=pk)
    context = {'cartitem': cartitem}
    return render(request, 'cartitem_detail.html', context)


def order_list(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order_list.html', context)


def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    context = {'order': order}
    return render(request, 'order_detail.html', context)


def orderdetail_list(request):
    orderdetails = OrderDetail.objects.all()
    context = {'orderdetails': orderdetails}
    return render(request, 'orderdetail_list.html', context)


def orderdetail_detail(request, pk):
    orderdetail = OrderDetail.objects.get(pk=pk)
    context = {'orderdetail': orderdetail}
    return render(request, 'orderdetail_detail.html', context)


def add_to_cart(request):
    if request.method == "POST":
     form = CartForm(request.POST)
    if form.is_valid():
            product = form.clean_data['product']
            quantity = form.clean_data['quantity']
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart.add_item(product, quantity)
            return redirect('cart')
    else:
        form = CartForm()
    return render(request, 'add_to_cart.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def stockbalance_list(request):
    stockbalances = StockBalance.objects.all()
    context = {'stockbalances': stockbalances}
    return render(request, 'stockbalance_list.html', context)


def stockbalance_detail(request, pk):
    stockbalance = StockBalance.objects.get(pk=pk)
    context = {'stockbalance': stockbalance}
    return render(request, 'stockbalance_detail.html', context)
