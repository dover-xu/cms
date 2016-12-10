"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from cms import settings
from focus import urls as focus_urls
from focus import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
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
    url(r'^focus/', include(focus_urls)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
