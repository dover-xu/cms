from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contents/$', views.contents.as_view(), name='contents'),
    url(r'^ucenter/$', views.ucenter.as_view(), name='ucenter'),
    url(r'^details/$', views.details.as_view(), name='details'),
    url(r'^publish/$', views.publish.as_view(), name='publish'),
    url(r'^a-c/$', views.add_comment.as_view(), name='add_comment'),
    url(r'^a-p-t-s/$', views.add_praise_tread_share.as_view(), name='add_praise_tread_share'),
    url(r'^del/$', views.del_note, name='del_note'),
    url(r'^del-n-c/$', views.del_note_comment.as_view(), name='del_note_comment'),
    url(r'^note-jx/$', views.note_jx.as_view(), name='note_jx'),
]
