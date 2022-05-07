from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from zoo.models import ModelCV
from . import models


class ZooHome(ListView):
    model = ModelCV
    template_name = 'zoo/index.html'
    context_object_name = 'models'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Model Zoo'
        return context

    def get_queryset(self):
        return models.ModelCV.objects.order_by('name')
