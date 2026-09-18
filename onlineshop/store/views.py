from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Product
from .models import Category
from.models import Order
from.models import OrderItem
from.models import Product
from.forms import OrderForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm



def product_list(request):
    query = request.GET.get('q')  
    products = Product.objects.all()

    if query:
        products = products.filter(
            models.Q(title__icontains=query) |
            models.Q(description__icontains=query)
        )

    categories = Category.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': None,
        'query': query,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    return render(request, 'store/product_list.html', {
        'products': products,
        'selected_category': category,
        'categories': Category.objects.all()
    })

def add_to_cart(request, pk):
    cart = request.session.get('cart', {})

    product = Product.objects.get(pk=pk)
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id]['quantity'] += 1
        cart[product_id]['subtotal'] = float(cart[product_id]['subtotal'] + product.price)
    else:
        cart[product_id] = {
            'quantity': 1,
            'subtotal': float(product.price)
        }

    request.session['cart'] = cart
    return redirect('product_list')


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, item in cart.items():
        product = Product.objects.get(pk=product_id)
        quantity = item['quantity']
        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart_detail')


def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')  

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for product_id, item in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product = product,
                    quantity=item['quantity']
                )
            request.session['cart'] = {}  
            request.session.modifed = True
            return redirect('order_success')
    else:
        form = OrderForm()

    total = sum(item['subtotal'] for item in cart.values())
    return render(request, 'store/checkout.html', {
        'form': form,
        'total': total
    })


def order_success(request):
    return render(request, 'store/order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    order_items = OrderItem.objects.filter(order=order)

    return render(request, 'store/order_detail.html', {
        'order': order,
        'order_items': order_items,
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


