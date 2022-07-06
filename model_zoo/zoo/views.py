from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView

from model_zoo.wsgi import cv_registry

from . import models
from .forms import LoadImageForm
from .models import ModelCV, RequestCV


class ZooHome(ListView):
    model = ModelCV
    template_name = 'zoo/index.html'
    context_object_name = 'models'

    def get_queryset(self):
        return models.ModelCV.objects.order_by('name')


class CVPage(FormView):
    model = RequestCV
    form_class = LoadImageForm

    def form_valid(self, form, **kwargs) -> HttpResponse:
        request_cv = form.save(commit=False)
        model = cv_registry.get_algorithm_by_id(kwargs['id_model'])
        request_cv.model_id = ModelCV.objects.get(
            id=kwargs['id_model']
        ).pk
        request_cv.save()
        request_cv.output_img = model.predict(request_cv.input_img.url)
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


class FaceDetectionPage(CVPage):
    template_name = 'zoo/cv_models/face_detection.html'
    id_model = 1

    def form_valid(self, form, **kwargs) -> HttpResponse:
        return super().form_valid(form, id_model=FaceDetectionPage.id_model)


class FaceRecognitionPage(CVPage):
    template_name = 'zoo/cv_models/face_recognition.html'
    id_model = 2

    def form_valid(self, form, **kwargs) -> HttpResponse:
        return super().form_valid(form, id_model=FaceRecognitionPage.id_model)


class TextDetectionPage(CVPage):
    template_name = 'zoo/cv_models/text_detection.html'
    id_model = 3

    def form_valid(self, form, **kwargs) -> HttpResponse:
        return super().form_valid(form, id_model=TextDetectionPage.id_model)


class EmotionsRecognitionPage(CVPage):
    template_name = 'zoo/cv_models/emotions_recognition.html'
    id_model = 4

    def form_valid(self, form, **kwargs) -> HttpResponse:
        return super().form_valid(form,
                                  id_model=EmotionsRecognitionPage.id_model)


class ColorizePhotoPage(CVPage):
    template_name = 'zoo/cv_models/colorize_photo.html'
    id_model = 5

    def form_valid(self, form, **kwargs) -> HttpResponse:
        return super().form_valid(form,
                                  id_model=ColorizePhotoPage.id_model)


class CVResponse(DetailView):
    model = RequestCV
    template_name = 'zoo/cv_models/cv_response.html'
    context_object_name = 'response'
