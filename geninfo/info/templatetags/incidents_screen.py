from django import template
from ..models import Report, Incident

register = template.Library()


@register.simple_tag
def date_ajusted(pk_incident):

    report = Report.objects.get(pk=pk_incident)
    report = report.created_at.strftime("%d/%m/%Y às %H:%M Hrs.")

    return report


@register.simple_tag
def date_incident(pk_incident):

    incident = Incident.objects.get(pk=pk_incident)
    incident = incident.date_incident.strftime("%d de %b, %Y.")

    return incident


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
