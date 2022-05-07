from django.urls import path
from . import views


urlpatterns = [
    path('', views.ZooHome.as_view(), name='home'),
]