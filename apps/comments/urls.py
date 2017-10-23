from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^comments/(?P<id>\d+)$', views.show),
    url(r'^comment$', views.comment),
]
