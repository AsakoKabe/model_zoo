from django.urls import path

from . import views

urlpatterns = [
    path('', views.ZooHome.as_view(), name='home'),
    path('face_detection/', views.FaceDetectionPage.as_view(), name='face_detection'),
]
