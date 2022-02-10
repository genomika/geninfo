# pylint: disable=no-name-in-module import-error useless-suppression
from os import environ

from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.views.generic.base import RedirectView

from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views as authtoken_views
from rest_framework.routers import DefaultRouter

from geninfo.info import views


app_name = "info"


def get_custom_schema_view():
    try:
        env_url = environ["API_URL"]
        schema_view = get_schema_view(
            openapi.Info(
                title="Geninfo API",
                default_version="v1",
                description="Geninfo API Docummentation",
            ),
            url=env_url,
            public=True,
            permission_classes=[permissions.AllowAny],
        )
    except KeyError:
        schema_view = get_schema_view(
            openapi.Info(
                title="Geninfo API",
                default_version="v1",
                description="Geninfo API Docummentation",
            ),
            public=True,
            permission_classes=[permissions.AllowAny],
        )
    return schema_view


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
    path(
        "api/docs",
        get_custom_schema_view().with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("api/login/", authtoken_views.obtain_auth_token),
]
