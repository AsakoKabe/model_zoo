from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, ListView, DetailView

from . import models
from .forms import LoadImageForm
from .models import ModelCV, RequestCV


class ZooHome(ListView):
    model = ModelCV
    template_name = 'zoo/index.html'
    context_object_name = 'models'

    def get_queryset(self):
        return models.ModelCV.objects.order_by('name')


class FaceDetectionPage(FormView):
    model = RequestCV
    template_name = 'zoo/cv_models/face_detection.html'
    form_class = LoadImageForm
    # success_url = reverse_lazy("cv_response")

    def form_valid(self, form) -> HttpResponse:
        request_cv = form.save(commit=False)
        request_cv.response = request_cv.input_img
        request_cv.model_id = ModelCV.objects.get(id=1).pk
        request_cv.save()
        self.obj_id = request_cv.pk
        return super().form_valid(form)

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Handle POST requests."""
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse("model_zoo:cv_response", kwargs={"pk": self.obj_id})


class CVResponse(DetailView):
    model = RequestCV
    template_name = 'zoo/cv_models/cv_response.html'
    context_object_name = 'response'

    # def get_queryset(self):
    #     return models.ModelCV.objects.order_by('name')
