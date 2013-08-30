from django.conf import settings

def expose_settings(request):
    """A context processor to expose settings in templates."""
    return {'settings': settings}