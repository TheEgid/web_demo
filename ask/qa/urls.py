from django.conf.urls import url, include
from django.urls import path
from qa.views import page, popular_page, question, test


urlpatterns = [
	url(r'^page/', page, name='page'),
	url(r'^$', page, name='page'),

	url(r'^popular/', popular_page, name='popular'),

	url(r'^login/', test, name='login'),
	url(r'^signup/', test, name='signup'),
	path('question/<slug:slug>/', question, name='question'),
	#url(r'^question/<slug:slug>/', question, name='question'),
	url(r'^ask/', test, name='ask'),

	url(r'^new/', test, name='new'),
]

