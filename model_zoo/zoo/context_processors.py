from . import models as model


def models(request):
    """
    Get models list.
    """
    return {"models": sorted(list(model.ModelCV.objects.all()),
                             key=lambda x: x.name)}
