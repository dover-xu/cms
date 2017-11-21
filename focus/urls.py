from django.conf.urls import url, include
from . import views
from rest_framework import routers
# from rest_framework.schemas import get_schema_view
router = routers.DefaultRouter()
router.register(r'api/model/Users', views.MyUserViewSet)
router.register(r'api/model/Notes', views.NoteViewSet)
router.register(r'api/model/Comments', views.CommentViewSet)
router.register(r'api/model/Praises', views.PraiseViewSet)
router.register(r'api/model/Treads', views.TreadViewSet)
router.register(r'api/model/Shares', views.ShareViewSet)
# schema_view = get_schema_view(title='Example API')

urlpatterns = [
    # url(r'^(?P<article_id>[0-9]+)/praise/$', views.get_praise_article, name='praise'),
    url(r'^api/contents/$', views.contents.as_view(), name='contents'),
    url(r'^api/ucenter/$', views.ucenter.as_view(), name='ucenter'),
    url(r'^api/details/$', views.details, name='details'),
    url(r'^api/publish/$', views.publish, name='publish'),
    url(r'^api/a-c/$', views.add_comment, name='add_comment'),
    url(r'^api/a-p-t-s/$', views.add_praise_tread_share, name='add_praise_tread_share'),
    url(r'^api/del/$', views.del_note, name='del_note'),
    
    url(r'^$', views.index, name='index'),

    url(r'^docs/', views.SwaggerSchemaView.as_view(), name='docs'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^api$', schema_view, name='api-root'),
    # url(r'^api/\.(?P<format>[a-z0-9]+)/?$', schema_view, name='api-root'),
]
urlpatterns += router.urls
