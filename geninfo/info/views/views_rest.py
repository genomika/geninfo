from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from geninfo.info import serializers
from geninfo.info.models import Incident


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = serializers.IncidentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == "retrieve":
            return serializers.IncidentDetailSerializer
        return self.serializer_class

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the incidents"""
        services = self.request.query_params.get("services")
        status = self.request.query_params.get("status")
        queryset = self.queryset
        if services:
            service_ids = self._params_to_ints(services)
            queryset = queryset.filter(services__id__in=service_ids)
        if status:
            queryset = queryset.filter(status_incident=status)

        return queryset

    @action(methods=["POST"], detail=True, url_path="close")
    def close(self, request, pk=None):
        """Close the incident"""
        incident = self.get_object()
        serializer = serializers.CloseSerializer(data=request.data)
        if serializer.is_valid():
            incident.finish_date_incidente = serializer.validated_data["finish_date"]
            incident.status_incident = "rs"
            if serializer.validated_data.get("description_report"):
                incident.reports.create(
                    description_report=serializer.validated_data["description_report"],
                    obs_report=serializer.validated_data["detail_report"],
                )
            incident.save()
            inc_ser = self.get_serializer(incident)
            return Response(inc_ser.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=True, url_path="report")
    def report(self, request, pk=None):
        """Append a report to the incident"""
        incident = self.get_object()
        serializer = serializers.ReportSerializer(data=request.data)
        if serializer.is_valid():
            incident.reports.create(
                description_report=serializer.validated_data["description_report"],
                obs_report=serializer.validated_data["obs_report"],
            )
            incident.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
