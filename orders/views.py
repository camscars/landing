from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created 
from cart.cart import Cart
# Create your views here.

def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order,
										product=item['product'],
										price=item['price'],
										quantity=item['quantity'])
			cart.clear()
			#the delay method launches the email task asynchronously
			order_created.delay(order.id)
			request.session['order_id'] = order.id #
			returnredirect(reverse('payment:process')) #redirect to payment
	else:
			form = OrderCreateForm()
	return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})

