from django.conf.urls import url
from django.conf import settings
from geninfo.info import views
from django.views.generic.base import RedirectView
from django.urls import include, path

urlpatterns = [
    path('', views.get_home),
    path('all_incidents/', views.get_home_incidents),
    url(r'^all_incidents/incidents_reports/(?P<pk>.+)/$', views.get_incidents),
    url(r'^incidents_reports/(?P<pk>.+)/$', views.get_incidents),
    url(r'^favicon.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),
]