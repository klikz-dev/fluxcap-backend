from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

from rest_framework import routers
from settings.views import AlertViewSet, RecordViewSet, SiteViewSet, TagViewSet, ZoneViewSet

router = routers.DefaultRouter()
router.register(r'sites', SiteViewSet)
router.register(r'tags', TagViewSet)
router.register(r'zones', ZoneViewSet)
router.register(r'records', RecordViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include('dj_rest_auth.urls')),
    path('api/', include(router.urls)),
]
