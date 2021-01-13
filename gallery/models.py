from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	sampleImage = models.ImageField(null=True, blank=True, upload_to='sample_images')
	image = models.ImageField(null=True, blank=True, upload_to='product_images')

	def __str__(self):
		return self.name

	@property
	def sampleImageURL(self):
		try:
			url = self.sampleImage.url
		except:
			url = ''
		return url

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
	
	
class OwnedItem(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	date_purchased = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([1 for item in orderitems])
		return total

	@property
	def get_added_items(self):
		addeditems = list(self.orderitem_set.values('product_id'))
		print(addeditems)
		return addeditems

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price
		return total
	

