from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'
    verbose = 'Payment'

    def ready(self):
    	import payment.signals

    	