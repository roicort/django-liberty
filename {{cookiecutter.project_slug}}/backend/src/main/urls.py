from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from api import urls as api_urls

urlpatterns = [
    # OpenAPI Schema
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # API
    path("api/", include(api_urls)),
    # Admin
    path("djadmin/", admin.site.urls),
    # Headless Account API
    path("api/auth/", include("allauth.headless.urls")),
    # Accounts
    path("account/", include("allauth.urls")),
    # OIDC
    path("", include("allauth.idp.urls")),
]
