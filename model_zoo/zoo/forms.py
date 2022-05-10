from django.forms import ModelForm, FileInput

from . import models


class LoadImageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoadImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.RequestCV
        fields = [
            "input_img",
        ]

        widgets = {
            "input_img": FileInput(
                attrs={
                    "id": "id_input_img",
                    "onchange": "handleFiles(this.files)",
                    "multiple accept": "image/*",
                })
        }
