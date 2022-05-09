from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from zoo.models import ModelCV, RequestCV

from . import models
from .forms import LoadImageForm


class ZooHome(ListView):
    model = ModelCV
    template_name = 'zoo/index.html'
    context_object_name = 'models'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return models.ModelCV.objects.order_by('name')


class FaceDetectionPage(FormView):
    template_name = 'zoo/cv_models/face_detection.html'
    form_class = LoadImageForm
    success_url = reverse_lazy("face_detection")
