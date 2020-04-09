from django.conf.urls import url
from django.urls import include, path

from qa.views import page, popular_page, question, ask
from qa.views import test, logout, user_login, signup


urlpatterns = [
    url(r'^ask/', ask, name='ask'),
    url(r'^page/', page, name='page'),
    url(r'^$', page, name='page'),
    url(r'^popular/', popular_page, name='popular'),
    url(r'^login/$', user_login, name='login'),
    url(r'^signup/', signup, name='signup'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^test/', test, name='test'),
    path(r'question/<slug:slug>/', question, name='question'),
]
