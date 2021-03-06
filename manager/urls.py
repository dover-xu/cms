from django.conf.urls import url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^signup/$', views.signup.as_view(), name='signup'),
    url(r'^login/$', views.log_in.as_view(), name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^user-state/$', views.user_state, name='user_state'),
    url(r'^setting/$', views.setting.as_view(), name='setting'),

    url(r'^api/auth/uname/$', views.auth_name, name='auth_name'),
    url(r'^api/activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.activate_user, name='active_user'),
    # url(r'^(?P<article_id>[0-9]+)/praise/$', views.get_praise_article, name='praise'),
]
urlpatterns += router.urls
