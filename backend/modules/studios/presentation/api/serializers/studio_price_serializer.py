from rest_framework import serializers

from modules.studios.infrastructure.persistence.models import StudioPrice


class StudioPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioPrice
        exclude = ["studio"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        valid_from = attrs.get("valid_from")
        valid_until = attrs.get("valid_until")
        if valid_until and valid_from and valid_until < valid_from:
            raise serializers.ValidationError(
                "The validity end date must not precede the start date."
            )
        return attrs
