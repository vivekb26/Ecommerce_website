from typing import Text
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
	customer = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)

	def __str__(self):
		return self.name
		# this show in admin panel in customer with each user name  

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_desc = models.TextField()
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product_name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=True)
	transction_id = models.CharField(max_length=200, null=True)

	@property
	def get_cart_total(self):
		ordered_items= self.orderitem_set.all()
		total = sum([item.get_total for item in ordered_items])
		return total

	@property
	def get_cart_items(self):
		cart_items = self.orderitem_set.all()
		total = sum([item.quantity for item in cart_items])
		return total

	def __str__(self):
		return str(self.id)

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0,null=True , blank= True)
	date_added = models.DateField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.product_price * self.quantity
		return total

	

	# def __str__(self):
    #     return Product.objects.get()

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=SET_NULL, blank=True, null=True)
	address = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=200, null=True)
	zipcode = models.CharField(max_length=200, null=True)
	country = models.CharField(max_length=200, null=True)
	date_added = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.address



