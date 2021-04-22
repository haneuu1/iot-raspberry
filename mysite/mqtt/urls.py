from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from mqtt.views import MqttDataViewSet

# app_name = 'mqtt'

router = routers.DefaultRouter()
router.register('', MqttDataViewSet)

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),
    # path('<int:pk>/', DetailView.as_view(), name='detail'),
    # path('log/', log, name='log'),
    # url(r'^admin/', admin.site.urls),
    url(r'^',include(router.urls)),
]