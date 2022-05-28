from . import models as model


def models(request):
    """
    Get models list.
    """
    return {"models": model.ModelCV.objects.all()}
