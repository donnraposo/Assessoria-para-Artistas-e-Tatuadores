from rest_framework import serializers


class CancellationDecisionSerializer(serializers.Serializer):
    approved = serializers.BooleanField()
    reason = serializers.CharField(max_length=2000, allow_blank=True, required=False)
