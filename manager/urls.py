from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^api/auth/uname/$', views.auth_name, name='auth_name'),
    url(r'^api/activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.activate_user, name='active_user'),
    # url(r'^(?P<article_id>[0-9]+)/praise/$', views.get_praise_article, name='praise'),
]
