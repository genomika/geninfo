# pylint: disable=too-many-return-statements

from django import template
from django.utils import timezone

from ..models import Incident, Service


register = template.Library()


@register.simple_tag
def overall_incident():

    incident = Incident.objects.all()
    overall = 0
    time_on = timezone.now()
    month_current = time_on.strftime("%m")

    for object_incident in incident:
        month_incident = object_incident.date_incident.strftime("%m")
        if month_incident == month_current:
            overall = overall + 1

    if overall > 0:
        return overall
    return "Sem incidentes"


@register.simple_tag
def incident_day(incident_object):
    incident = Incident.objects.get(name_incident=incident_object)

    date_now_incident = incident.date_incident
    date_now_incident = date_now_incident.strftime("%d")

    return date_now_incident


@register.simple_tag
def date_current():
    date_on_day = timezone.now().strftime("%d/%m/%Y")
    return date_on_day


@register.simple_tag
def date_incident_in():
    incident = Incident.objects.all()

    response = []
    for inc_day in incident:
        response.append(inc_day.date_incident.strftime("%d/%m/%Y"))
    return response


@register.simple_tag
def duration_incident(incident_object):
    incident = Incident.objects.get(number_incident=incident_object)
    date1 = incident.date_incident
    date2 = incident.last_date_incident

    date_duration = date2 - date1
    minutos = str(date_duration).split(":")[1]
    minutos = minutos.split(".")
    minutos = int(minutos[0])

    date_duration_hour = str(date_duration).split(":")[0]
    try:
        if incident.status_incident == "rs":
            if date_duration.days > 1:
                return str(date_duration.days) + " Dias"

            if date_duration.days == 1:
                return str(date_duration.days) + " Dia"

            if date_duration.days < 1:
                if date_duration_hour == "0":
                    return str(minutos) + " Minutos"
                if date_duration_hour == "1":
                    return date_duration_hour + " Hora"
                return date_duration_hour + " Horas"
        return " - "
    except Exception:  # pylint: disable=broad-except
        return "-"


@register.simple_tag
def status_service(number):
    service = Service.objects.get(pk=number)
    total_incidents = service.incidents_affected.filter(
        status_incident__in=["pe", "en"]
    ).count()

    if total_incidents > 0:
        return True
    return False


@register.simple_tag
def last_report(incident_object):
    incident = Incident.objects.get(number_incident=incident_object)

    last_incident_report = incident.reports.last()
    if last_incident_report:
        return last_incident_report
    return "Sem atualizações"
