import json
from .models import *

def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	items = []
	order = {'get_cart_total':0, 'get_cart_items': 0}
	cartItems = order['get_cart_items']

	for i in cart:
		try: 
			cartItems += 1

			product = Product.objects.get(pk=i)

			order['get_cart_total'] += product.price
			order['get_cart_items'] += 1

			item = {
				'product': {
					'id': product.id,
					'name': product.name,
					'price': product.price,
					'sampleImageURL': product.sampleImageURL,
					'imageURL': product.imageURL,
				},
				'get_total': product.price
			}

			items.append(item)
		except:
			pass

	return {'items': items, 'order': order, 'cartItems': cartItems}

def cartData(request):
	if request.user.is_authenticated:
		customer, created = Customer.objects.get_or_create(user=request.user)
		customer.name = request.user.username
		customer.email = request.user.email
		customer.save()
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		cookieData = cookieCart(request)
		if cookieData['cartItems'] != 0:
			cookieItems = cookieData['items']
			items = []
			cartItems = cookieData['cartItems']

			for item in cookieItems:
				product = Product.objects.get(pk=item['product']['id'])
				orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
				orderItem.save()
				items.append(item)
				
			items = order.orderitem_set.all()
			cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'items': items, 'order': order, 'cartItems': cartItems}


def guestOrder(request, data):
	print('User is not logged in')

	print('COOKIES:', request.COOKIES)
	name = data['form']['name']
	email = data['form']['email']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
		email = email, 
		)

	customer.name = name
	customer.save()

	order = Order.objects.create(
		customer = customer,
		complete = False,
		)

	for item in items:
		product = Product.objects.get(pk=item['product']['id'])

		orderItem = OrderItem.objects.create(
			product = product,
			order = order,
			)
	return customer, order