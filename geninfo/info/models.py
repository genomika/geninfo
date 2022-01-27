import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, pre_save

from .mail import send_email_notification_closed, send_email_notification_open


INFO_CHOICES = (("op", "Operacional"), ("nop", "Não Operacional"))

IMPACT_CHOICES = (("le", "Leve"), ("mo", "Moderado"), ("gv", "Grave"))

TYPE_CHOICES = (("co", "Corretivo"), ("pv", "Preventivo"))

STATUS_CHOICES = (("pe", "Pendente"), ("en", "Em Análise"), ("rs", "Resolvido"))


def increment_id():
    last_id = Incident.objects.all().order_by("number_incident").last()
    if not last_id:
        return (
            str(datetime.date.today().year)
            + str(datetime.date.today().month).zfill(2)
            + "0000"
        )
    ultimo_id = last_id.number_incident
    ultimo_int = int(ultimo_id[8:14])
    new_int = ultimo_int + 1
    new_id = (
        str(str(datetime.date.today().year))
        + str(datetime.date.today().month).zfill(2)
        + str(new_int).zfill(4)
    )
    return new_id


# def take_date(self):
#     date_take = Incident.objects.all()

#     if not date_take.finish_date_incidente:
#         if date_take.status_incident == 'pe' or date_take.status_incident == 'en':
#             return None
#         elif date_take.status_incident == 'rs':
#             time_on = timezone.now()
#             return time_on


class Report(models.Model):
    description_report = models.CharField(verbose_name="Relatório", max_length=65)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        verbose_name="Usuário",
        null=True,
        on_delete=models.SET_NULL,
        related_name="reports",
    )
    # status_report = models.CharField(choices=STATUS_CHOICES, verbose_name="Status Relatório",
    # default="pe", max_length=30, editable=True)
    obs_report = models.TextField(verbose_name="Descrição do Relátorio", max_length=400)
    created_at = models.DateTimeField(
        verbose_name="Criado em", auto_now_add=True, editable=False
    )
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL)
    target = GenericForeignKey(
        "content_type",
        "object_id",
    )

    class Meta:
        verbose_name = u"Relatório"
        verbose_name_plural = u"Relatórios"

    def __str__(self):
        return self.description_report


class Service(models.Model):
    name = models.CharField(verbose_name=u"Nome do Serviço", max_length=30)
    status_service = models.CharField(
        choices=INFO_CHOICES,
        verbose_name="Status do Serviço",
        default="op",
        max_length=30,
    )

    class Meta:
        verbose_name = u"Serviço"
        verbose_name_plural = u"Serviços"

    def __str__(self):
        return self.name


class Incident(models.Model):
    number_incident = models.CharField(
        max_length=300, default=increment_id, editable=False
    )
    name_incident = models.CharField(verbose_name="Nome do incidente", max_length=30)
    status_incident = models.CharField(
        choices=STATUS_CHOICES,
        verbose_name="Status do Incidente",
        default="pe",
        max_length=30,
    )
    incident_occurrence = models.CharField(
        choices=TYPE_CHOICES,
        max_length=30,
        default="co",
        verbose_name="Tipo do incidente",
    )
    incident_impact = models.CharField(
        choices=IMPACT_CHOICES,
        max_length=30,
        default="le",
        verbose_name="Gravidade do incidente",
    )
    finish_date_incidente = models.DateTimeField(
        verbose_name="Data de Conclusão", null=True, blank=True
    )
    date_incident = models.DateTimeField(
        verbose_name="Data de inicio", auto_now_add=True
    )
    last_date_incident = models.DateTimeField(
        verbose_name="Ultima atualização", auto_now=True
    )
    description = models.TextField(
        verbose_name="Descrição do incidente", max_length=400
    )
    # duration_incident = models.CharField(verbose_name="Duração do incidente", max_length=30)
    services_afted = models.ManyToManyField(
        Service, verbose_name="Serviços afetados", related_name="incidents_affected"
    )

    reports = GenericRelation(Report)

    class Meta:
        verbose_name = u"Incidente"
        verbose_name_plural = u"Incidentes"

    def __str__(self):
        return self.name_incident


post_save.connect(send_email_notification_open, sender=Incident)
pre_save.connect(send_email_notification_closed, sender=Incident)

# Create your models here.
