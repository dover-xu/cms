from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^(?P<article_id>[0-9]+)/praise/$', views.get_praise_article, name='praise'),
    url(r'^$', views.index, name='index'),
    url(r'^index-hot$', views.index_hot, name='index_hot'),
    url(r'^index-new$', views.index_new, name='index_new'),
    url(r'^video$', views.video, name='video'),
    url(r'^video-hot$', views.video_hot, name='video_hot'),
    url(r'^video-new$', views.video_new, name='video_new'),
    url(r'^pic$', views.pic, name='pic'),
    url(r'^pic-hot$', views.pic_hot, name='pic_hot'),
    url(r'^pic-new$', views.pic_new, name='pic_new'),
    url(r'^jape$', views.jape, name='pic'),
    url(r'^jape-hot$', views.jape_hot, name='jape_hot'),
    url(r'^jape-new$', views.jape_new, name='jape_new'),
    url(r'^user/focus/publish$', views.user_publish, name='user_publish'),
    url(r'^user/focus/share$', views.user_share, name='user_share'),
    url(r'^user/focus/comment$', views.user_comment, name='user_comment'),
    url(r'^user/publish/video$', views.publish_video, name='publish_video'),
    url(r'^user/publish/pic$', views.publish_pic, name='publish_pic'),
    url(r'^user/publish/jape$', views.publish_jape, name='publish_jape'),
    url(r'^api/auth/uname/$', views.auth_name, name='auth_name'),
]
