from django.conf.urls import url
from django.urls import path


from qa.views import page, popular_page, question, ask
from qa.views import test, user_login, register

urlpatterns = [
    url(r'^page/', page, name='page'),
    url(r'^$', page, name='page'),
    url(r'^popular/', popular_page, name='popular'),

    # path('account/', account, name='account'),
    path('account_regist/', register, name='register'),
    # path('login/', user_login, name='login'),

    url(r'^login/$', user_login, name='login'),

    url(r'^signup/', register, name='signup'),

    path(r'question/<slug:slug>/', question, name='question'),

    url(r'^ask/', ask, name='ask'),
    # url(r'^new/', test, name='new'),
]
