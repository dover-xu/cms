from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login(?P<url>[0-9]+)$', views.log_in, name='login'),
    url(r'^logout$', views.log_out, name='logout'),
    # url(r'^(?P<article_id>[0-9]+)/praise/$', views.get_praise_article, name='praise'),
]
