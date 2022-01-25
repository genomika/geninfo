from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from .models import Incident, Service


def get_home(request):
    services = Service.objects.all()
    incidents = Incident.objects.all()

    date_on_day = timezone.now()
    date_seven_days = timedelta(days=7)
    diff_today = date_on_day - date_seven_days

    incidents_filter = Incident.objects.filter(date_incident__gte=diff_today).order_by(
        "last_date_incident"
    )

    _async = request.GET.get("async", None)
    if _async:
        template = "tr_home.html"

    template = "home.html"
    return render(
        request,
        template,
        {
            "services": services,
            "incidents": incidents,
            "incidents_filter": incidents_filter,
        },
    )


def get_home_incidents(request):
    services = Service.objects.all()
    incidents = Incident.objects.all().order_by("last_date_incident")

    _async = request.GET.get("async", None)
    if _async:
        template = "tr_home.html"

    template = "all_incidents.html"
    return render(request, template, {"services": services, "incidents": incidents})


def get_incidents(request, pk):
    incidents = Incident.objects.get(pk=pk)
    template = "incidents.html"
    return render(request, template, {"incidents": incidents})


# Create your views here.
