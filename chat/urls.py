from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^thread/(?P<pk>\d+)/$', views.thread, name='thread'),

    # API

    url(r'^(?P<pk>\d+)/send/$', views.send_message, name='send_message'),
]
