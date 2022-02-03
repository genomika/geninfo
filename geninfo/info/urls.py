from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import RedirectView

from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from geninfo.info import views


app_name = "info"

schema_view = get_schema_view(
    title="Geninfo API", renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer]
)

router = DefaultRouter()
router.register("incidents", views.views_rest.IncidentViewSet)

urlpatterns = [
    path("", views.views_web.get_home),
    path("all_incidents/", views.views_web.get_home_incidents),
    url(
        r"^all_incidents/incidents_reports/(?P<pk>.+)/$", views.views_web.get_incidents
    ),
    url(r"^incidents_reports/(?P<pk>.+)/$", views.views_web.get_incidents),
    url(
        r"^favicon.ico$",
        RedirectView.as_view(url=settings.STATIC_URL + "images/favicon.ico"),
    ),
    path("api/", include(router.urls)),
    url("api/docs", schema_view),
]
