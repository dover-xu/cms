from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework.schemas import get_schema_view
router = routers.DefaultRouter()
router.register(r'Users', views.MyUserViewSet)
router.register(r'Notes', views.NoteViewSet)
router.register(r'Comments', views.CommentViewSet)
router.register(r'Praises', views.PraiseViewSet)
router.register(r'Treads', views.TreadViewSet)
router.register(r'Shares', views.ShareViewSet)
schema_view = get_schema_view(title='Example API')

urlpatterns = [
    # url(r'^(?P<article_id>[0-9]+)/praise/$', views.get_praise_article, name='praise'),
    url(r'^contents/$', views.contents.as_view(), name='contents'),
    url(r'^ucenter/$', views.ucenter.as_view(), name='ucenter'),
    url(r'^details/$', views.details, name='details'),
    url(r'^publish/$', views.publish, name='publish'),
    url(r'^api/a-c/$', views.add_comment, name='add_comment'),
    url(r'^api/a-p-t-s/$', views.add_praise_tread_share, name='add_praise_tread_share'),

    # 以下是基于django模板的
    url(r'^$', views.index, name='index'),

    # url(r'^index-new$', views.index_new, name='index_new'),
    # url(r'^video$', views.video, name='video'),
    # url(r'^video-hot$', views.video_hot, name='video_hot'),
    # url(r'^video-new$', views.video_new, name='video_new'),
    # url(r'^pic$', views.pic, name='pic'),
    # url(r'^pic-hot$', views.pic_hot, name='pic_hot'),
    # url(r'^pic-new$', views.pic_new, name='pic_new'),
    # url(r'^jape$', views.jape, name='pic'),
    # url(r'^jape-hot$', views.jape_hot, name='jape_hot'),
    # url(r'^jape-new$', views.jape_new, name='jape_new'),

    url(r'^$', views.index, name='index'),
    url(r'^detail_(?P<note_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^user/focus/publish$', views.user_publish, name='user_publish'),
    url(r'^user/focus/share$', views.user_share, name='user_share'),
    url(r'^user/focus/comment$', views.user_comment, name='user_comment'),
    url(r'^user/publish/video$', views.publish_video, name='publish_video'),
    url(r'^user/publish/pic$', views.publish_pic, name='publish_pic'),
    url(r'^user/publish/jape$', views.publish_jape, name='publish_jape'),
    url(r'^api/del$', views.del_note, name='del_note'),

    url(r'^docs/', views.schema_view),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/$', schema_view, name='api-root'),
    url(r'^api/\.(?P<format>[a-z0-9]+)/?$', schema_view, name='api-root'),
]
urlpatterns += router.urls
