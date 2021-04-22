from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from recording.views import RecordingDataViewSet

# app_name = 'recording'

router = routers.DefaultRouter()
router.register('', RecordingDataViewSet)

urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail')
    # url(r'^admin/', admin.site.urls),
    url(r'^',include(router.urls)),
]

