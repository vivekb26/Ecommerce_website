import json
import datetime
from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse
from django.views.generic import (
    ListView
)
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        cartitems = order.get_cart_items

    else:
        order = {
            'get_cart_total' : 0,
            'get_cart_items' : 0,
        }
        cartitems = ['get_cart_items']

    context = {
    'cartitems' : cartitems,
    'product' : Product.objects.all(),
    'order' : order,

    }
    return render(request,'ecom/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items

    else:
        items = []
        order = {
            'get_cart_total' : 0,
            'get_cart_items' : 0,
        }
        cartitems = ['get_cart_items']

    context = {
    'cartitems' : cartitems,
    'items' : items,
    'order' : order,
    }
    return render(request,'ecom/cart.html',context)
    
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items

    else:
        items = []
        order = {
            'get_cart_total' : 0,
            'get_cart_items' : 0,
        }
        cartitems = ['get_cart_items']

    context = {
        'cartitems' : cartitems,
        'items' : items,
        'order' : order,
    }
    return render(request,'ecom/checkout.html', context)

def product_detail(request,pk):
    context = {
    'product' : Product.objects.get(pk=pk)
    }
    return render(request,'ecom/product_detail.html',context)

class ProductListView(ListView):
    model = Product
    template_name = 'ecom/store.html'
    context_object_name = 'product'

    
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print("action:", action)
    print("productId:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)

def processOrder(request):
    transction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        total = float(data['form']['total'])
        order.transction_id = transction_id

        # this is important to prevent user from changing value or price manually through javascript
        if total == order.get_cart_total:
            order.complete =True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order =order,
            address= data["shipping"]["address"],
            city= data["shipping"]["city"],
            country= data["shipping"]["country"],
            zipcode= data["shipping"]["zipcode"],
        )

    else:
        print("user not logged in")


    return JsonResponse('payment done', safe=False)
