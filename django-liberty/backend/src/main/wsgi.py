import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE", "main.settings.base"),
)

application = get_wsgi_application()
application = WhiteNoise(application, root=settings.STATIC_ROOT)
