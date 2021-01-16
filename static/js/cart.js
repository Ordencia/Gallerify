var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; ++i) {
	updateBtns[i].addEventListener('click', function() {
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId: ', productId, 'action: ', action)

		console.log('user: ', user)
		
		if (user != 'AnonymousUser') {
			updateUserOrder(productId, action)
		} else {
			addCookieItem(productId, action)
		}
		
	})
}

function updateCart(productId, action) {
	var cart_num = parseInt(document.getElementById('cart-total').innerHTML, 10)

	if (action == 'add') {
		if (cart[productId] == undefined) {
			cart[productId] = 1
			cart_num += 1
		}
	}

	if (action == 'remove') {
		var cart_total = parseFloat(document.getElementsByClassName('cart-data')[1].innerHTML.substring(1))
		if (cart[productId]) {
			price = parseFloat(document.getElementById(productId).getElementsByTagName('strong')[0].innerHTML.substring(1))
			cart_total -= price
			cart_num -= 1
			delete cart[productId]

			document.getElementById(productId).classList.add('hidden')
			document.getElementsByClassName('cart-data')[0].innerHTML=cart_num.toString()
			document.getElementsByClassName('cart-data')[1].innerHTML="$"+cart_total.toFixed(2).toString()
		}
	}

	document.getElementById('cart-total').innerHTML=cart_num.toString()
}

function addCookieItem(productId, action) {
	updateCart(productId, action)

	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

function updateUserOrder(productId, action) {
	console.log('User is logged in')

	var url = '/update_item/'

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({'productId': productId, 'action': action})
	})

	.then((response) => {
		return response.json()
	})

	.then((data) => {
		console.log('data: ', data)
		
		addCookieItem(productId, action)
	})
}