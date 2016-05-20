from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):

	def __init__(self, request):
		#Initialize cart
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			# save empty cart in session
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def __len__(self):
		#Count items in cart
		return sum(item['quantity'] for item in self.cart.values())

	def __iter__(self):
		#iterate through items in cart and retrive products from database
		product_ids = self.cart.keys()
		#get product objects and add to cart
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def add(self, product, quantity=1, update_quantity=False):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
		
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity	
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def save(self):
		# update cart in session
		self.session[settings.CART_SESSION_ID] = self.cart
		# mark the session as "modified"
		self.session.modified = True

	def remove(self, product):
		#remove from cart
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		#Remove the cart from the session
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True