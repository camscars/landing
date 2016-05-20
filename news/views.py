from django.shortcuts import render, redirect
from .models import Article, Feed
from .forms import FeedForm

import feedparser
import datetime
# Create your views here.


def articles_list(request):
	articles = Article.objects.all()
	# create a rows of 2 articles each
	rows = [articles[x:x+1] for x in range(0, len(articles), 1)]


	return render(request, 'news/article_list.html', {'rows':rows})

def feeds_list(request):
	feeds = Feed.objects.all()
	return render(request, 'news/feed_list.html', {'feeds':feeds})

def new_feed(request):
	if request.method == "POST":
		form = FeedForm(request.POST)
		if form.is_valid():
			feed = form.save(commit=False)
			
			existingFeed = Feed.objects.filter(url = feed.url) # stop duplicates
			if len(existingFeed) == 0:

				feedData = feedparser.parse(feed.url)
				feed.title = feedData.feed.title
				feed.save()

				for entry in feedData.entries:
					article = Article()
					article.title = entry.title
					article.url = entry.link
					article.description = entry.description
					d = datetime.datetime(*(entry.published_parsed[0:6])) #cuts off all of the seconds and miliseconds and such
					dateString = d.strftime('%Y-%m-%d %H:%M:%S')

					article.publication_date = dateString
					article.feed = feed
					article.save()

			return redirect('news.views.feeds_list')
	else:
		form = FeedForm()
	return render(request, 'news/new_feed.html', {'form':form})