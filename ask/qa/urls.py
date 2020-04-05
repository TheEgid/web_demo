from django.conf.urls import url
from django.urls import path
from qa.views import page, popular_page, question, ask, test


urlpatterns = [
	url(r'^page/', page, name='page'),
	url(r'^$', page, name='page'),
	url(r'^popular/', popular_page, name='popular'),

	url(r'^login/', test, name='login'),
	url(r'^signup/', test, name='signup'),

	path(r'question/<slug:slug>/', question, name='question'),

	url(r'^ask/', ask, name='ask'),
	# url(r'^new/', test, name='new'),
]

