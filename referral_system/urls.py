from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="ReferralSystemAPI",
        default_version="v1",
        description="Referral System Backend API Endpoints.",
    ),
    public=True,
)

urlpatterns = [
    path(
        "doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/auth/", include("custom_auth.urls")),
    path("api/", include("core.urls")),
]
