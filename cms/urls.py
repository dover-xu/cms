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
from django.conf.urls import url, include
from cms import settings
from focus import views
from rest_framework.schemas import get_schema_view
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'model/Users', views.MyUserViewSet)
router.register(r'model/Notes', views.NoteViewSet)
router.register(r'model/Comments', views.CommentViewSet)
router.register(r'model/Praises', views.PraiseViewSet)
router.register(r'model/Treads', views.TreadViewSet)
router.register(r'model/Shares', views.ShareViewSet)

schema_view = get_schema_view(title='Core API')

urlpatterns = [
                url(r'^docs/', views.SwaggerSchemaView.as_view(), name='docs'),
                url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                # url(r'^api/$', schema_view, name='api-root'),
                # url(r'^api/\.(?P<format>[a-z0-9]+)/?$', schema_view, name='api-root'),

                url(r'^admin/', admin.site.urls),
                url(r'^manager/', include('manager.urls')),
                url(r'^api/', include('focus.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += router.urls
