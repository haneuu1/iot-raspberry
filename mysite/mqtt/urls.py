from django.urls import path
from mqtt.views import *

app_name = 'mqtt'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('log/', log, name='log'),
]