from rest_framework import serializers


class CancellationInputSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=2000)
