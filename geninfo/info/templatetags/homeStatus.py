from django import template
from ..models import Incident, Service, Report
from django.utils import timezone
import datetime
from datetime import datetime, date
import time
import math

register = template.Library()

@register.simple_tag
def overall_incident():

    incident = Incident.objects.all()
    overall = 0
    time_on = timezone.now()
    month_current = time_on.strftime('%m')

    for object_incident in incident:
        month_incident = object_incident.date_incident.strftime('%m')
        if month_incident == month_current:
            overall = overall + 1

    try:
        if overall > 0:
            return overall
    except:
        return 'Sem incidentes'


@register.simple_tag
def incident_day(incident_object):

    incident = Incident.objects.get(name_incident=incident_object)
    date_on = timezone.now().strftime('%d')

    response = []
    date_now_incident = incident.date_incident
    date_now_incident = date_now_incident.strftime('%d')
    print(date_on)


    return date_now_incident

@register.simple_tag
def date_current():
    date_on_day = timezone.now().strftime('%d/%m/%Y')
    print(date_on_day)
    return date_on_day

@register.simple_tag
def date_incident_in():
    incident = Incident.objects.all()

    response = []
    for incident_day in incident:
       response.append(incident_day.date_incident.strftime('%d/%m/%Y'))
       print(incident_day)
    return response

@register.simple_tag
def duration_incident(incident_object):
    incident = Incident.objects.get(number_incident=incident_object)
    date1 = incident.date_incident
    date2 = incident.last_date_incident

    date_duration = date2 - date1
    minutos = str(date_duration).split(':')[1]
    minutos = minutos.split('.')
    minutos = int(minutos[0])

    date_duration_hour = str(date_duration).split(':')[0]

    try:
        if incident.status_incident == 'rs':
            if date_duration.days > 1:
                return str(date_duration.days) + ' Dias'
            
            if date_duration.days == 1:
                return str(date_duration.days) + ' Dia'

            if date_duration.days < 1:
                if date_duration_hour == '0':
                    return str(minutos) + ' Minutos'
                if date_duration_hour == '1':
                    return date_duration_hour + ' Hora'
                return date_duration_hour + ' Horas'
        else:
            return ' - '
    except:
        return '-'

@register.simple_tag
def status_service(number):
    service = Service.objects.get(pk=number)
    total_incidents = service.incidents_affected.filter(status_incident__in=['pe','en']).count()

    if total_incidents > 0:
        return True
    return False

    '''
    incident_in = Incident.objects.get(number_incident=number)
    size_incidentes = incident_in.services_afted.count()
    if incident_in.status_incident == 'en' or incident_in.status_incident == 'pe':
        if size_incidentes > 0:
            return True
        else:
            return False
    '''

@register.simple_tag
def last_report(incident_object):
    incident = Incident.objects.get(number_incident=incident_object)

    last_report = incident.reports.last()
    if last_report:
        return last_report
    else:
        return 'Sem atualizações'