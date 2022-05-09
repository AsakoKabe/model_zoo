from django.forms import ModelForm

from . import models


class LoadImageForm(ModelForm):

    class Meta:
        model = models.RequestCV
        fields = [
            "input_img",
        ]

        widgets = {

        }
