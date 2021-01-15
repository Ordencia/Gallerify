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

function addCookieItem(productId, action) {
	console.log("hello")
	if (action == 'add') {
		if(cart[productId] == undefined) {
			cart[productId] = 1
		}
	}

	if (action == 'remove') {
		if (cart[productId]) {
			delete cart[productId]
		}
	}

	console.log('Cart: ', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
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
		location.reload()
	})
}