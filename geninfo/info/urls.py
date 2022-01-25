from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views.generic.base import RedirectView

from geninfo.info import views


urlpatterns = [
    path("", views.get_home),
    path("all_incidents/", views.get_home_incidents),
    url(r"^all_incidents/incidents_reports/(?P<pk>.+)/$", views.get_incidents),
    url(r"^incidents_reports/(?P<pk>.+)/$", views.get_incidents),
    url(
        r"^favicon.ico$",
        RedirectView.as_view(url=settings.STATIC_URL + "images/favicon.ico"),
    ),
]
