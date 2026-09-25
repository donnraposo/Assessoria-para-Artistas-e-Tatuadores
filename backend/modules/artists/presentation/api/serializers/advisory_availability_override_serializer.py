from rest_framework import serializers


class AdvisoryAvailabilityOverrideSerializer(serializers.Serializer):
    starts_at = serializers.DateTimeField()
    ends_at = serializers.DateTimeField()
    timezone = serializers.CharField(max_length=64)
    reason = serializers.CharField()
