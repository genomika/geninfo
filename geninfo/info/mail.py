from django.core.mail import send_mail, EmailMessage
# from .models import Incident

# envio de email com template
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string


from django.db import transaction

def release_notes():
    template_name = "release.html"
    message_html = render_to_string(template_name)
    subject = "Release 0.1.1"
    from_email = "lucas@genomika.com.br"
    msg = EmailMessage(subject, message_html, from_email, ['lucas@genomika.com.br'])
    msg.send(fail_silently=False)

def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner

@on_transaction_commit
def send_email_notification_open(sender, instance, **kwargs):
    created = kwargs.get('created')
    
    if not created:
        return
    
    status = instance.status_incident
    incident_name = instance.name_incident
    description = instance.description
    affectds = []

    for affected in instance.services_afted.all():
        affected_out = affected.name
        affectds.append(affected_out)
    
    subject = '[ATENÇÃO] Incidente aberto nos sistemas[ %s ]' % ', '.join(affectds)
    from_email = 'notificacoes@genomika.com.br'
    to_teste = 'lucas@genomika.com.br'
    to = 'colaboradores@genomika.com.br'
    fail_silently = False

    context = {'incident_name': instance.name_incident,'number_incident': instance.number_incident, 
               'affectds': ', '.join(affectds), 'description': description, 'objects_incidents' : instance.pk}

    template_name = 'email_alert.html'
    message_html = render_to_string(template_name, context)
    message_txt = striptags(message_html)
    email = EmailMultiAlternatives(subject=subject, body=message_txt, from_email=from_email,to=[to])
    email.attach_alternative(message_html, "text/html")

    if status == 'pe':
        email.send(fail_silently=False)

def send_email_notification_closed(sender, instance, **kwargs):

    status = instance.status_incident
    incident_name = instance.name_incident
    description = instance.description
    affectds = []

    if instance.id is None:
        pass
    else:
        current = instance
        previus = sender.objects.get(id=instance.id)
        if previus.status_incident != current.status_incident:
            if current.status_incident == 'rs':

                for affected in instance.services_afted.all():
                    affected_out = affected.name
                    affectds.append(affected_out)
                
                subject = '[ATENÇÃO] Incidente Nº: '+instance.number_incident+' encerrado nos sistemas [ %s ]' % ', '.join(affectds)
                from_email = 'notificacoes@genomika.com.br'
                to_teste = 'lucas@genomika.com.br'
                to = 'colaboradores@genomika.com.br'
                fail_silently = False

                context = {'incident_name': instance.name_incident,'number_incident': instance.number_incident, 
                        'affectds': ', '.join(affectds), 'description': description, 'objects_incidents': instance.pk, 'date_time': instance.finish_date_incidente}

                template_name = 'closed_alert.html'
                message_html = render_to_string(template_name, context)
                message_txt = striptags(message_html)
                email = EmailMultiAlternatives(subject=subject, body=message_txt, from_email=from_email,to=[to])
                email.attach_alternative(message_html, "text/html")


                email.send(fail_silently=False)