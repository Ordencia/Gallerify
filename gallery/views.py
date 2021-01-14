from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
import requests
import webbrowser
from decimal import Decimal

from .models import *
from .utils import *

# Create your views here.


def store(request):

	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items
	# else:
	# 	items = []
	# 	order = {'get_cart_total':0, 'get_cart_items': 0}
	# 	cartItems = order['get_cart_items']

	products = Product.objects.all()

	data = cartData(request)
	cartItems = data['cartItems']

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'gallery/store.html', context)

def cart(request):

	context = cartData(request)
	return render(request, 'gallery/cart.html', context)

def checkout(request):

	context = cartData(request)
	return render(request, 'gallery/checkout.html', context)

def repo(request):

	data = cartData(request)
	cartItems = data['cartItems']

	if request.user.is_authenticated:
		customer = request.user.customer
		items = customer.owneditem_set.all()
	else:
		items = []

	context = {'items':items, 'cartItems':cartItems}
	return render(request, 'gallery/repo.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	print('Action:', action)
	print('productId:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	orderItem.save()

	if action == 'remove':
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	items = data['items']
	prefix = data['url']

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else:
		customer, order = guestOrder(request, data)

	total = Decimal(data['form']['total'])

	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True

		if request.user.is_authenticated:
			for item in items:
				ownedItem, created = OwnedItem.objects.get_or_create(customer=customer, product=Product.objects.get(pk=item['product_id']))
				ownedItem.save()


	order.save()

	return JsonResponse('Payment complete', safe=False)
