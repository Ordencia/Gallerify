import json
from .models import *

def cookieCart(request):
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}

	print('hello Cart: ', cart)
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
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'items': items, 'order': order, 'cartItems': cartItems}