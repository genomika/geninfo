from django.contrib.auth import get_user_model

from rest_framework import serializers

from geninfo.info.models import Incident, Report, Service


class CloseSerializer(serializers.Serializer):
    finish_date = serializers.DateTimeField()
    description_report = serializers.CharField(max_length=65, required=False)
    detail_report = serializers.CharField(max_length=400, required=False)

    def validate(self, attrs):
        """
        Check both required fields for report exists.
        """

        if attrs.get("description_report") and not attrs.get("detail_report"):
            raise serializers.ValidationError(
                "Detail report must exist to create a report."
            )
        if attrs.get("detail_report") and not attrs.get("description_report"):
            raise serializers.ValidationError(
                "Description report must exist to create a report."
            )
        return attrs

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class ReportSerializer(serializers.ModelSerializer):
    """
    Serializar for a report object
    """

    class Meta:
        model = Report
        fields = ("object_id", "description_report", "obs_report", "created_at")
        read_only_fields = ("object_id",)


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for an service object"""

    class Meta:
        model = Service
        fields = ("id", "name", "status_service")
        read_only_fields = ("id",)


class ReportRelatedField(serializers.RelatedField):
    """
    Custom field to use for the report generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, Report):
            serializer = ReportSerializer(value)
        else:
            raise Exception("Unexpected type of tagged object")

        return serializer.data

    def to_internal_value(self, data):
        report_class = Report.objects.filter(pk=data)
        if report_class and (len(report_class)) == 1:
            return report_class.get()
        raise serializers.ValidationError(f"Report with pk: {data} not found")


class IncidentSerializer(serializers.ModelSerializer):
    """
    Serialize an Incident
    """

    services_afted = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Service.objects.all()
    )
    reports = ReportRelatedField(many=True, queryset=Report.objects.all())

    def create(self, validated_data):
        services_data = validated_data.pop("services_afted")
        reports_data = validated_data.pop("reports")
        incident = Incident.objects.create(**validated_data)
        incident.services_afted.set(services_data)
        incident.reports.set(reports_data)
        return incident

    def update(self, instance, validated_data):
        services_data = validated_data.pop("services_afted", None)
        reports_data = validated_data.pop("reports", None)
        if services_data is not None:
            instance.services_afted.set(services_data)
        if reports_data is not None:
            instance.reports.set(reports_data)
        return super().update(instance, validated_data)

    def validate_finish_date_incidente(self, value):
        new = self.instance is None
        if new:
            msg = "Finish date cannot be for a new instance."
            raise serializers.ValidationError(msg)
        return value

    def get_status_incident_display(self, obj):
        return obj.get_status_incident_display()

    class Meta:
        model = Incident
        depth = 2
        fields = (
            "id",
            "number_incident",
            "name_incident",
            "incident_occurrence",
            "incident_impact",
            "finish_date_incidente",
            "date_incident",
            "status_incident",
            "get_status_incident_display",
            "last_date_incident",
            "description",
            "reports",
            "services_afted",
        )
        read_only_fields = ("id",)


class IncidentDetailSerializer(IncidentSerializer):
    """Serialize an incident detail"""

    services_afted = ServiceSerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)
