from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.articles_list, name='news_list'),
	url(r'^feeds/$', views.feeds_list, name='feeds_list'),
	url(r'^feeds/new', views.new_feed, name='feed_new'),
]