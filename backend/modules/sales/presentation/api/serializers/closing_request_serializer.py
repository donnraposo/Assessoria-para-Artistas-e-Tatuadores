from rest_framework import serializers


class ClosingRequestSerializer(serializers.Serializer):
    appointment_id = serializers.UUIDField()
    final_value = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)
    currency = serializers.RegexField(regex=r"^[A-Z]{3}$")
    artist_minimum_approved = serializers.BooleanField(default=False)
    payment_reference = serializers.CharField(max_length=160)
    idempotency_key = serializers.CharField(max_length=120)
