from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from . import models
from .forms import LoadImageForm
from .models import ModelCV


class ZooHome(ListView):
    model = ModelCV
    template_name = 'zoo/index.html'
    context_object_name = 'models'

    def get_queryset(self):
        return models.ModelCV.objects.order_by('name')


class FaceDetectionPage(FormView):
    template_name = 'zoo/cv_models/face_detection.html'
    form_class = LoadImageForm
    success_url = reverse_lazy("face_detection")
