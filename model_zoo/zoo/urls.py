from django.urls import path

from . import views

app_name = "model_zoo"
urlpatterns = [
    path('', views.ZooHome.as_view(), name='home'),
    path('face-detection/', views.FaceDetectionPage.as_view(),
         name='face_detection'),
    path('face-recognition/', views.FaceRecognitionPage.as_view(),
         name='face_recognition'),
    path('text-detection/', views.TextDetectionPage.as_view(),
         name='text-detection'),
    path('cv-response/<int:pk>/', views.CVResponse.as_view(),
         name='cv_response'),
]
