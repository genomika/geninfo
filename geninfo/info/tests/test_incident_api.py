import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient

from geninfo.info.models import Incident, Report, Service
from geninfo.info.serializers import IncidentDetailSerializer, IncidentSerializer


INCIDENTS_URL = reverse("info:incident-list")


def detail_url(incident_id):
    """Return incident detail URL"""
    return reverse("info:incident-detail", args=[incident_id])


def close_url(incident_id):
    """Return URL for close the incident"""
    return reverse("info:incident-close", args=[incident_id])


def append_url(incident_id):
    """Return URL for appending a report the incident"""
    return reverse("info:incident-report", args=[incident_id])


class PublicIncidentApiTests(TestCase):
    """Test unauthenticated incident API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(INCIDENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIncidentApiTests(TestCase):
    """Test authenticated Incident access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@test.com", "testpass")
        self.incidents = baker.make(Incident, _quantity=3, make_m2m=True)
        self.client.force_authenticate(self.user)

    def test_retrieve_incidents(self):
        """Test retrieving list of incidents"""
        res = self.client.get(INCIDENTS_URL)
        serializer = IncidentSerializer(self.incidents, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_view_incident_detail(self):
        """Test viewing an incident detail"""
        reports_set = baker.make(Report, _quantity=2)
        single_incident = baker.make(Incident, reports=reports_set, make_m2m=True)
        url = detail_url(single_incident.id)
        res = self.client.get(url)
        serializer = IncidentDetailSerializer(single_incident)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_incident(self):
        """Test creating incident"""
        payload = {
            "name_incident": "Simple Incident",
            "incident_occurrence": "co",
            "incident_impact": "le",
            "status_incident": "pe",
            "description": "Simple incident test",
        }

        res = self.client.post(INCIDENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        incident = Incident.objects.get(id=res.data["id"])
        for key in payload:
            self.assertEqual(payload[key], getattr(incident, key))

    def test_create_incident_with_services(self):
        """Test creating incident with services"""
        single_service = baker.make(Service)
        second_service = baker.make(Service)

        payload = {
            "name_incident": "Huge Incident",
            "incident_occurrence": "co",
            "services_afted": [single_service.id, second_service.id],
            "incident_impact": "mo",
            "status_incident": "pe",
            "description": "Simple incident test",
        }

        res = self.client.post(INCIDENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        incident = Incident.objects.get(id=res.data["id"])
        services = incident.services_afted.all()
        self.assertEqual(services.count(), 2)
        self.assertIn(single_service, services)
        self.assertIn(second_service, services)

    def test_create_incident_with_services_reports(self):
        """Test creating incident with services and reports"""
        single_service = baker.make(Service)
        second_service = baker.make(Service)

        report_service = baker.make(Report)

        payload = {
            "name_incident": "Report Incident",
            "incident_occurrence": "co",
            "services_afted": [single_service.id, second_service.id],
            "reports": [report_service.id],
            "incident_impact": "mo",
            "status_incident": "pe",
            "description": "Simple incident test",
        }

        res = self.client.post(INCIDENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        incident = Incident.objects.get(id=res.data["id"])
        reports = incident.reports.all()
        self.assertEqual(reports.count(), 1)
        self.assertIn(report_service, reports)

    def test_partial_update_incident(self):
        services_set = baker.prepare(Service, _quantity=2)
        single_incident = baker.make(
            Incident, services_afted=services_set, make_m2m=True
        )

        payload = {"status_incident": "en"}
        url = detail_url(single_incident.id)
        self.client.patch(url, payload)

        single_incident.refresh_from_db()
        self.assertEqual(single_incident.status_incident, payload["status_incident"])
        services = single_incident.services_afted.all()
        self.assertEqual(len(services), 2)

    def test_full_update_incident(self):
        services_set = baker.make(Service, _quantity=2)
        single_report, second_report = baker.make(Report, _quantity=2, make_m2m=True)
        single_incident = baker.make(
            Incident,
            reports=[single_report],
            services_afted=services_set,
            make_m2m=True,
        )
        currdate = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        payload = {
            "name_incident": single_incident.name_incident,
            "description": single_incident.description,
            "status_incident": "rs",
            "reports": [single_report.id, second_report.id],
            "finish_date_incidente": currdate,
        }

        url = detail_url(single_incident.id)
        self.client.put(url, payload)
        single_incident.refresh_from_db()
        self.assertEqual(single_incident.status_incident, payload["status_incident"])
        self.assertEqual(
            single_incident.finish_date_incidente.strftime("%Y-%m-%dT%H:%M:%S"),
            payload["finish_date_incidente"],
        )
        reports = single_incident.reports.all()
        self.assertEqual(len(reports), 2)
        self.assertIn(second_report, reports)
        services = single_incident.services_afted.all()
        self.assertEqual(len(services), 0)

    def test_filter_incidents_by_status(self):
        """Test returning incident with specific statuses"""
        several_open_incidents = baker.make(
            Incident, _quantity=5, status_incident="en", make_m2m=True
        )
        several_closed_incidents = baker.make(
            Incident, _quantity=5, status_incident="rs", make_m2m=True
        )

        res = self.client.get(INCIDENTS_URL, {"status": "en"})
        serialized_open_data = [
            IncidentSerializer(incident) for incident in several_open_incidents
        ]
        serialized_closed_data = [
            IncidentSerializer(incident) for incident in several_closed_incidents
        ]

        for ser_data in serialized_open_data:
            self.assertIn(ser_data.data, res.data["results"])
        for ser_not_data in serialized_closed_data:
            self.assertNotIn(ser_not_data.data, res.data["results"])

    def test_filter_incidents_by_services(self):
        """Test returning incident with specific services"""
        several_open_incidents = baker.make(
            Incident, _quantity=5, status_incident="en", make_m2m=True
        )
        several_closed_incidents = baker.make(
            Incident, _quantity=5, status_incident="rs", make_m2m=True
        )

        res = self.client.get(INCIDENTS_URL, {"status": "en"})
        serialized_open_data = [
            IncidentSerializer(incident) for incident in several_open_incidents
        ]
        serialized_closed_data = [
            IncidentSerializer(incident) for incident in several_closed_incidents
        ]

        for ser_data in serialized_open_data:
            self.assertIn(ser_data.data, res.data["results"])
        for ser_not_data in serialized_closed_data:
            self.assertNotIn(ser_not_data.data, res.data["results"])

    def test_close_basic_incident(self):
        "Test closing an incident"
        single_incident = baker.make(Incident, status_incident="en", make_m2m=True)
        currdate = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        url = close_url(single_incident.id)
        payload = {"finish_date": currdate}
        res = self.client.post(url, payload)
        single_incident.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            single_incident.finish_date_incidente.strftime("%Y-%m-%dT%H:%M:%S"),
            payload["finish_date"],
        )
        self.assertEqual(single_incident.status_incident, "rs")

    def test_close_incident_with_report(self):
        "Test closing an incident"
        single_incident = baker.make(Incident, status_incident="en", make_m2m=True)
        currdate = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        url = close_url(single_incident.id)
        payload = {
            "finish_date": currdate,
            "description_report": "Simple Close Report.",
            "detail_report": "Simple Detail Report.",
        }
        res = self.client.post(url, payload)
        single_incident.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            single_incident.finish_date_incidente.strftime("%Y-%m-%dT%H:%M:%S"),
            payload["finish_date"],
        )
        self.assertEqual(single_incident.status_incident, "rs")
        report = single_incident.reports.latest("created_at")
        self.assertEqual(report.description_report, payload["description_report"])
        self.assertEqual(report.obs_report, payload["detail_report"])

    def test_append_report(self):
        "Test appending a report to incident"
        single_incident = baker.make(Incident, status_incident="en", make_m2m=True)

        url = append_url(single_incident.id)
        payload = {
            "description_report": "Simple Close Report.",
            "obs_report": "Simple Detail Report.",
        }
        res = self.client.post(url, payload)
        single_incident.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        report = single_incident.reports.latest("created_at")
        self.assertEqual(report.description_report, payload["description_report"])
        self.assertEqual(report.obs_report, payload["obs_report"])
