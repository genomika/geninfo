from django.contrib import admin
from .models import Service, Incident, Report
from django.contrib.contenttypes.admin import GenericStackedInline
from .forms import IncidentForm

from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string

from django.http import HttpResponse
import csv
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

def incident_report(modelAdmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Incidentes.csv"'
    writeIncidentCSV = csv.writer(response, delimiter=',')

    # CABECALHO
    writeIncidentCSV.writerow(['Numero do incidente', 'Nome do incidente', 'Data de inicio',
                                'Data de conclusão','Status do incidente', 'Tipo do incidente',
                                'Descrição do incidente', 'Serviços afetados', 'Gravidade do incidente'])
    
    for incident in queryset:
        number = incident.number_incident
        name = incident.name_incident
        date_initial = incident.date_incident
        date_finish = incident.finish_date_incidente
        status = incident.get_status_incident_display()
        type_incident = incident.incident_occurrence
        description = incident.description
        impact = incident.get_incident_impact_display()
        

        for affected in incident.services_afted.all():
            affected_in = affected.name

        
        writeIncidentCSV.writerow([number, name, date_initial, date_finish, status, type_incident,
                                   description, affected_in, impact])

    return response

incident_report.short_description = 'Download do Relatorio'

def send_email_open(modelAdmin, request, queryset):
    for incident in queryset:
        status = incident.status_incident
        incident_name = incident.name_incident
        description = incident.description
        affectds = []

        for affected in incident.services_afted.all():
            affected_out = affected.name
            affectds.append(affected_out)
    
        subject = '[ATENÇÃO] Incidente aberto nos sistemas[ %s ]' % ', '.join(affectds)
        from_email = 'notificacoes@genomika.com.br'
        to_teste = 'lucas@genomika.com.br'
        to = 'colaboradores@genomika.com.br'
        fail_silently = False

        context = {'incident_name': incident.name_incident,'number_incident': incident.number_incident, 
                'affectds': ', '.join(affectds), 'description': description, 'objects_incidents' : incident.pk}

        template_name = 'email_alert.html'
        message_html = render_to_string(template_name, context)
        message_txt = striptags(message_html)
        email = EmailMultiAlternatives(subject=subject, body=message_txt, from_email=from_email,to=[to])
        email.attach_alternative(message_html, "text/html")

        if status == 'pe':
            email.send(fail_silently=False)

send_email_open.short_description = 'Enviar email de abertura'

def send_email_closed(modelAdmin, request, queryset):
    for incident in queryset:
        print('entrei')
        status = incident.status_incident
        incident_name = incident.name_incident
        description = incident.description
        affectds = []

        if status == 'rs':
            for affected in incident.services_afted.all():
                affected_out = affected.name
                affectds.append(affected_out)
            
            subject = '[ATENÇÃO] Incidente Nº: '+incident.number_incident+' encerrado nos sistemas [ %s ]' % ', '.join(affectds)
            from_email = 'notificacoes@genomika.com.br'
            to_teste = 'lucas@genomika.com.br'
            to = 'colaboradores@genomika.com.br'
            fail_silently = False

            context = {'incident_name': incident.name_incident,'number_incident': incident.number_incident, 
                    'affectds': ', '.join(affectds), 'description': description, 'objects_incidents': incident.pk, 'date_time': incident.finish_date_incidente}

            template_name = 'closed_alert.html'
            message_html = render_to_string(template_name, context)
            message_txt = striptags(message_html)
            email = EmailMultiAlternatives(subject=subject, body=message_txt, from_email=from_email,to=[to])
            email.attach_alternative(message_html, "text/html")


            email.send(fail_silently=False)

send_email_closed.short_description = 'Enviar email de encerramento'

class ServiceAdmin(admin.ModelAdmin):
    list_display=('name', 'status_service')

class ReportAdminInline(GenericStackedInline):
    model = Report
    extra = 0
    # fields = ['description_report', 'user']
    readonly_fields = ['user', 'created_at']
    # suit_classes = 'suit-tab suit-tab-general'

class IncidentAdmin(admin.ModelAdmin):
    list_display = ('number_incident', 'finish_date_incidente', 'status_incident', 'name_incident','date_incident', 
                    'last_date_incident')
    inlines = [ReportAdminInline]
    form = IncidentForm
    actions = [send_email_open, send_email_closed, incident_report]

    def changelist_view(self, request, extra_context=None):
        if 'action' in request.POST and request.POST['action'] == 'incident_report':
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Incident.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(IncidentAdmin, self).changelist_view(request, extra_context)


admin.site.register(Service, ServiceAdmin)
admin.site.register(Incident, IncidentAdmin)
# Register your models here.
