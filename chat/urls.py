from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^thread/with/(?P<username>.*)/$', views.thread, name='thread'),

    # API

    url(r'^(?P<username>.*)/send/$', views.send_message, name='send_message'),
]
