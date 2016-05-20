import os
import celery
from django.conf import settings

#set default django settings for 'celery program'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'landing.settings')

app = Celery('landing')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

print celery.__file__